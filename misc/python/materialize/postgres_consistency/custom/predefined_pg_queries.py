# Copyright Materialize, Inc. and contributors. All rights reserved.
#
# Use of this software is governed by the Business Source License
# included in the LICENSE file at the root of this repository.
#
# As of the Change Date specified in that file, in accordance with
# the Business Source License, use of this software will be governed
# by the Apache License, Version 2.0.


from materialize.output_consistency.data_type.data_type import DataType
from materialize.output_consistency.enum.enum_constant import (
    StringConstant,
)
from materialize.output_consistency.execution.value_storage_layout import (
    ValueStorageLayout,
)
from materialize.output_consistency.expression.expression import (
    Expression,
    LeafExpression,
)
from materialize.output_consistency.expression.expression_with_args import (
    ExpressionWithArgs,
)
from materialize.output_consistency.input_data.operations.boolean_operations_provider import (
    AND_OPERATION,
    NOT_OPERATION,
)
from materialize.output_consistency.input_data.operations.set_operations_provider import (
    create_in_operation,
)
from materialize.output_consistency.input_data.operations.text_operations_provider import (
    LOWER_OPERATION,
    REGEXP_REPLACE,
    TEXT_NOT_LIKE_OPERATION,
)
from materialize.output_consistency.input_data.types.boolean_type_provider import (
    BOOLEAN_DATA_TYPE,
)
from materialize.output_consistency.input_data.types.date_time_types_provider import (
    INTERVAL_TYPE,
)
from materialize.output_consistency.input_data.types.text_type_provider import (
    TEXT_DATA_TYPE,
)
from materialize.output_consistency.query.query_template import QueryTemplate
from materialize.output_consistency.selection.selection import DataRowSelection


def create_custom_pg_consistency_queries() -> list[QueryTemplate]:
    return [create_pg_timezone_abbrevs_query(), create_pg_timezone_names_query()]


def create_pg_timezone_abbrevs_query() -> QueryTemplate:
    abbrev_col_expr = _create_simple_leaf_expression("abbrev", TEXT_DATA_TYPE)
    pg_timezone_abbrevs_cols: list[Expression] = [
        abbrev_col_expr,
        _create_simple_leaf_expression("utc_offset", INTERVAL_TYPE),
        _create_simple_leaf_expression("is_dst", BOOLEAN_DATA_TYPE),
    ]
    pg_timezone_abbrevs = QueryTemplate(
        expect_error=False,
        select_expressions=pg_timezone_abbrevs_cols,
        where_expression=None,
        storage_layout=ValueStorageLayout.VERTICAL,
        contains_aggregations=False,
        row_selection=DataRowSelection(),
        custom_db_object_name="pg_catalog.pg_timezone_abbrevs",
        custom_order_expressions=[abbrev_col_expr],
    )

    return pg_timezone_abbrevs


def create_pg_timezone_names_query() -> QueryTemplate:
    pg_timezone_name_col_expr = _create_simple_leaf_expression("name", TEXT_DATA_TYPE)
    pg_timezone_abbrev_col_expr = _create_simple_leaf_expression(
        "abbrev", TEXT_DATA_TYPE
    )
    pg_timezone_names_cols: list[Expression] = [
        pg_timezone_name_col_expr,
        pg_timezone_abbrev_col_expr,
        _create_simple_leaf_expression("utc_offset", INTERVAL_TYPE),
        _create_simple_leaf_expression("is_dst", BOOLEAN_DATA_TYPE),
    ]

    no_posix_timezones = ExpressionWithArgs(
        operation=TEXT_NOT_LIKE_OPERATION,
        args=[
            pg_timezone_name_col_expr,
            StringConstant("posix/%"),
        ],
    )

    # TODO #26521: time zones differ
    excluded_timezones = [
        # abbrev, utc_offset, is_dst differ
        "America/Godthab",
        "America/Nuuk",
        "Asia/Gaza",
        "Asia/Hebron",
        # abbrev differs
        "Europe/Kirov",
        "Europe/Volgograd",
    ]

    # do not exist in mz
    excluded_timezones.extend(
        [
            "Factory",
            "localtime",
            "posixrules",
        ]
    )

    # excluded because they cause pain with sorting
    excluded_timezones.extend(
        [
            "Etc/GMT+0",
            "Etc/GMT-0",
            "GMT+0",
            "GMT-0",
        ]
    )

    excluded_timezones_expr = ExpressionWithArgs(
        operation=NOT_OPERATION,
        args=[
            ExpressionWithArgs(
                operation=create_in_operation(len(excluded_timezones)),
                args=[
                    pg_timezone_name_col_expr,
                    *[StringConstant(tz) for tz in excluded_timezones],
                ],
            )
        ],
    )

    exclusion_expression = ExpressionWithArgs(
        operation=AND_OPERATION,
        args=[no_posix_timezones, excluded_timezones_expr],
    )

    # remove special characters for ordering due to different sort order
    order_by_sanitized_name_expr = ExpressionWithArgs(
        operation=LOWER_OPERATION,
        args=[
            ExpressionWithArgs(
                operation=REGEXP_REPLACE,
                args=[
                    pg_timezone_name_col_expr,
                    StringConstant("[^A-Za-z0-9]"),
                    StringConstant(""),
                    # all occurrences
                    StringConstant("g"),
                ],
            )
        ],
    )

    pg_timezone_names = QueryTemplate(
        expect_error=False,
        select_expressions=pg_timezone_names_cols,
        where_expression=exclusion_expression,
        storage_layout=ValueStorageLayout.VERTICAL,
        contains_aggregations=False,
        row_selection=DataRowSelection(),
        custom_db_object_name="pg_catalog.pg_timezone_names",
        custom_order_expressions=[
            order_by_sanitized_name_expr,
            pg_timezone_abbrev_col_expr,
        ],
    )

    return pg_timezone_names


def _create_simple_leaf_expression(
    column_name: str, data_type: DataType
) -> LeafExpression:
    return LeafExpression(
        column_name=column_name,
        data_type=data_type,
        characteristics=set(),
        storage_layout=ValueStorageLayout.VERTICAL,
    )
