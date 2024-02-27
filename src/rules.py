def validate(rules_df, project):
    errors = []

    for _, row in rules_df.iterrows():
        (comparator, operator, column) = row
        del operator
        table, column = column.split('.')

        _type = project.schema[table][column]['type']
        try:
            match _type:
                case 'INTEGER' | 'FLOAT':
                    float(comparator)
                case _:
                    pass
        except:  # pylint: disable=bare-except
            errors.append(
                f'Comparator value ({comparator}) is invalid for column {column} of type {_type}'
            )

    return errors
