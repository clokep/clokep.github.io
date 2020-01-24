from __future__ import absolute_import, print_function, unicode_literals

import tempfile

from django.db import connections, models
from django.db.models.fields import AutoField

import six


class LoadDataQuerySet(models.QuerySet):
    """A QuerySet with an additional load_data method which inserts data quickly in bulk."""

    def _convert_instance_to_line(self, fields, instance, connection):
        """Convert an object to a single line to be placed in the temporary file."""
        # Convert each field value to a database value.
        #
        # Escape the enclosure and escape characters since they are not handled
        # automatically.
        db_prep_values = [
            six.text_type(self.model._meta.get_field(field_name).get_db_prep_value(
                getattr(instance, field_name), connection)).replace('\\', '\\\\').replace('"', '\\"')
            for field_name in fields
        ]

        # Comma separate the wrapped values.
        return ','.join(map(lambda v: '"' + v + '"', db_prep_values)) + '\n'

    def load_data(self, objs):
        """
        Inserts each of the instances into the database. This does *not* call
        save() on each of the instances, does not send any pre/post save
        signals, and does not set the primary key attribute if it is an
        autoincrement field. Multi-table models are not supported.

        Write the data to a temporary file, then insert that data into MySQL via a LOAD DATA call.

        :param tuple fields: A tuple of string field names.
        :param list objs: The list of objects to insert.
        :returns: The number of inserted records.
        :rtype int:
        """

        # This is based on by bulk_create.
        self._for_write = True
        connection = connections[self.db]
        fields = self.model._meta.concrete_fields
        fields = [f.name for f in fields if not isinstance(f, AutoField)]

        # The table name and field names cannot be parameterized when executing
        # a SQL statement with the Django ORM. The name of the file where data
        # is loaded from can be parameterized, however.
        #
        # The result of this is a partially formatted string to be fed into MySQL.
        load_data_statement = """
            LOAD DATA LOCAL INFILE %s INTO TABLE {mysql_table_name} CHARACTER SET utf8 FIELDS TERMINATED BY ',' ENCLOSED BY '"' LINES TERMINATED BY '\\n' ({fields});
            """.format(
                mysql_table_name=self.model._meta.db_table,
                fields=', '.join(fields)
            ).strip()

        # Write each object to their own line in a temporary file and bulk
        # insert the data into MySQL using the LOAD DATA statement.
        with tempfile.NamedTemporaryFile(mode='w', suffix='.data', delete=True) as data_file:
            data_file.writelines(
                self._convert_instance_to_line(fields, obj, connection) for obj in objs
            )
            data_file.flush()

            with connection.cursor() as cursor:
                return cursor.execute(load_data_statement, [data_file.name])
