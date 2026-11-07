from dotenv import load_dotenv
import pg8000
import json
import os

from dependencies import _row_to_dict

load_dotenv(".env")
DB = os.getenv("DB_NAME")
USER = os.getenv("DB_USER")
PASS = os.getenv("DB_PASS")
HOST = os.getenv("DB_HOST")

class SupabaseClientWrapper:
    def __init__(self, database=DB, user=USER, password=PASS, host=HOST):
        self.conn_params = {
            "database": database,
            "user": user,
            "password": password,
            "host": host
        }

    def table(self, table_name: str):
        return QueryBuilder(self.conn_params, table_name)

    def _row_to_dict(self, columns, row):
        result = {}
        for col, val in zip(columns, row):
            # Convert UUID to string
            if hasattr(val, 'hex') and hasattr(val, 'int'):  # UUID check
                result[col] = str(val)
            else:
                result[col] = val
        return result

    def rpc(self, function_name: str, params: dict = None):
        conn = pg8000.connect(**self.conn_params)
        cursor = conn.cursor()
        
        if params:
            arg_slots = ", ".join([f"{k} := %s" for k in params.keys()])
            query = f"SELECT * FROM {function_name}({arg_slots});"
            args = tuple(params.values())
        else:
            query = f"SELECT * FROM {function_name}();"
            args = ()

        cursor.execute(query, args)
        try:
            columns = [desc[0] for desc in cursor.description]
            rows = [self._row_to_dict(columns, row) for row in result_rows]
        except:
            rows = []

        conn.commit()
        cursor.close()
        conn.close()

        class Response:
            data = rows
        return Response()


class QueryBuilder:
    def __init__(self, conn_params, table_name):
        self.conn_params = conn_params
        self.table_name = table_name
        self._action = "SELECT"
        self._select_clause = "*"
        self._update_data = {}
        self._insert_data = {}
        self._filters = []
        self._order_by = None
        self._limit = None
        self._offset = None
        self._single = False
        self._count = None

    def _row_to_dict(self, columns, row):
        result = {}
        for col, val in zip(columns, row):
            # Convert UUID to string
            if hasattr(val, 'hex') and hasattr(val, 'int'):  # UUID check
                result[col] = str(val)
            else:
                result[col] = val
        return result

    def select(self, columns: str = "*", count: int = "*"):
        self._action = "SELECT"
        self._select_clause = columns
        self._count = count # store count mode
        return self

    def update(self, data: dict):
        self._action = "UPDATE"
        self._update_data = data
        return self

    def delete(self):
        self._action = "DELETE"
        return self

    def insert(self, data: dict or list):
        self._action = "INSERT"
        self._insert_data = data
        return self  # ← Return self for chaining

#    def insert(self, data: dict or list):
#        conn = pg8000.connect(**self.conn_params)
#        cursor = conn.cursor()

#        records = data if isinstance(data, list) else [data]
#        if not records:
#            return self

#        columns = ", ".join(records[0].keys())
#        placeholders = ", ".join(["%s"] * len(records[0]))
#        query = f"INSERT INTO {self.table_name} ({columns}) VALUES ({placeholders}) RETURNING *"

#        rows = []
#        for record in records:
#            values = tuple(json.dumps(v) if isinstance(v, (dict, list)) else v for v in record.values())
#            cursor.execute(query, values)

            # Convert to dict with UUID handling
#            columns_result = [desc[0] for desc in cursor.description]
#            result_rows = cursor.fetchall()
#            rows.extend([self._row_to_dict(columns_result, row) for row in result_rows])  # ← changed

#        conn.commit()
#        cursor.close()
#        conn.close()

#        is_list = isinstance(data, list)
#        result = rows if is_list else (rows[0] if rows else None)

#        class Response:
#            data = result
#        return Response()

    # Filter methods (same as before)
    def eq(self, column: str, value):
        self._filters.append((f"{column} = %s", value))
        return self

    def neq(self, column: str, value):
        self._filters.append((f"{column} != %s", value))
        return self

    def gt(self, column: str, value):
        self._filters.append((f"{column} > %s", value))
        return self

    def gte(self, column: str, value):
        self._filters.append((f"{column} >= %s", value))
        return self

    def lt(self, column: str, value):
        self._filters.append((f"{column} < %s", value))
        return self

    def lte(self, column: str, value):
        self._filters.append((f"{column} <= %s", value))
        return self

    def like(self, column: str, pattern: str):
        self._filters.append((f"{column} LIKE %s", pattern))
        return self

    def ilike(self, column: str, pattern: str):
        self._filters.append((f"{column} ILIKE %s", pattern))
        return self

    def is_(self, column: str, value):
        if value is None:
            self._filters.append((f"{column} IS NULL", None))
        else:
            self._filters.append((f"{column} IS %s", value))
        return self

    def in_(self, column: str, values: list):
        self._filters.append((f"{column} IN %s", tuple(values)))
        return self

    def contains(self, column: str, value):
        if isinstance(value, (dict, list)):
            self._filters.append((f"{column} @> %s::jsonb", json.dumps(value)))
        else:
            self._filters.append((f"{column} @> %s", value))
        return self

    def order(self, column: str, desc: bool = False, nullsfirst: bool = False):
        direction = "DESC" if desc else "ASC"
        nulls = "NULLS FIRST" if nullsfirst else "NULLS LAST"
        self._order_by = f"ORDER BY {column} {direction} {nulls}"
        return self

    def single(self):
        self._single = True
        return self  # ← Return self for chaining

    def maybe_single(self):
        self._single = True
        return self

    def limit(self, count: int):
        self._limit = f"LIMIT {count}"
        return self

    def range(self, from_idx: int, to_idx: int):
        self._limit = f"LIMIT {to_idx - from_idx + 1}"
        self._offset = f"OFFSET {from_idx}"
        return self

    def execute(self):
        conn = pg8000.connect(**self.conn_params)
        cursor = conn.cursor()
        args = []

        if self._action == "SELECT":
            if self._count == "exact":
                query = f"SELECT COUNT(*) FROM {self.table_name}"
            else:
                query = f"SELECT {self._select_clause} FROM {self.table_name}"

            if self._filters:
                clauses = [f[0] for f in self._filters]
                query += " WHERE " + " AND ".join(clauses)
                for f in self._filters:
                    if f[1] is not None:
                        args.append(f[1])

            if self._count != "exact":
                if self._order_by:
                    query += f" {self._order_by}"
                if self._limit:
                    query += f" {self._limit}"
                if self._offset:
                    query += f" {self._offset}"

            cursor.execute(query, tuple(args))

            if self._count == "exact":
                count_result = cursor.fetchone()[0]
                conn.commit()
                cursor.close()
                conn.close()

                class CountResponse:
                    data = []
                    count = count_result
                return CountResponse()

            # Normal select
            columns = [desc[0] for desc in cursor.description]
            result_rows = cursor.fetchall()
            rows = [self._row_to_dict(columns, row) for row in result_rows]

            conn.commit()
            cursor.close()
            conn.close()

            if self._single:
                result = rows[0] if rows else None
                class Response:
                    data = result
                return Response()

            class Response:
                data = rows
            return Response()

        elif self._action == "INSERT":
            data = self._insert_data
            records = data if isinstance(data, list) else [data]

            columns = ", ".join(records[0].keys())
            placeholders = ", ".join(["%s"] * len(records[0]))
            query = f"INSERT INTO {self.table_name} ({columns}) VALUES ({placeholders}) RETURNING *"

            rows = []
            for record in records:
                values = tuple(
                    json.dumps(v) if isinstance(v, (dict, list)) else v 
                    for v in record.values()
                )
                cursor.execute(query, values)
                columns_result = [desc[0] for desc in cursor.description]
                result_rows = cursor.fetchall()
                rows.extend([self._row_to_dict(columns_result, row) for row in result_rows])

            conn.commit()
            cursor.close()
            conn.close()

            is_list = isinstance(data, list)
            result = rows

            class Response:
                data = result
            return Response()

        elif self._action == "UPDATE":
            set_clause = ", ".join([f"{k} = %s" for k in self._update_data.keys()])
            query = f"UPDATE {self.table_name} SET {set_clause}"
            for v in self._update_data.values():
                args.append(json.dumps(v) if isinstance(v, (dict, list)) else v)

        elif self._action == "DELETE":
            query = f"DELETE FROM {self.table_name}"

        if self._filters:
            clauses = [f[0] for f in self._filters]
            query += " WHERE " + " AND ".join(clauses)
            for f in self._filters:
                if f[1] is not None:
                    args.append(f[1])

        if self._action == "SELECT":
            if self._order_by:
                query += f" {self._order_by}"
            if self._limit:
                query += f" {self._limit}"
            if self._offset:
                query += f" {self._offset}"

        if self._action in ["UPDATE", "DELETE"]:
            query += " RETURNING *"

        cursor.execute(query, tuple(args))

        try:
            columns = [desc[0] for desc in cursor.description]
            result_rows = cursor.fetchall()
            rows = [self._row_to_dict(columns, row) for row in result_rows]
        except:
            rows = []

        conn.commit()
        cursor.close()
        conn.close()

        # Handle single() modifier
        if self._single:
            result = rows[0] if rows else None

            class Response:
                data = result
            return Response()

        class Response:
            data = rows

        return Response()


def create_client(url: str = "", key: str = ""):
    return SupabaseClientWrapper()
