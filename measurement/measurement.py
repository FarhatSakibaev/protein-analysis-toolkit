from config import AUTOLYSIS_UPPER_LIMIT_SIZE, AUTOLYSIS_LOWER_LIMIT_SIZE, NATIVE_LOWER_LIMIT_SIZE, \
    NATIVE_UPPER_LIMIT_SIZE, SMALL_AGGREGATES_LOWER_LIMIT_SIZE, SMALL_AGGREGATES_UPPER_LIMIT_SIZE, \
    LARGE_AGGREGATES_LOWER_LIMIT_SIZE, LARGE_AGGREGATES_UPPER_LIMIT_SIZE, EXCLUSION_LOWER_LIMIT, \
    EXCLUSION_UPPER_LIMIT, logger, DECIMAL_PLACES


class Measurement:

    def __init__(self, data: list, y_label_value) -> None:
        self.y_label_value = y_label_value
        self.groups_count = 0

        self.percentages = {
            'autolysis': [],
            'native': [],
            'small_aggregates': [],
            'large_aggregates': [],
        }

        self.row_count = 0

        self.calculations = {
            'autolysis': 0.0,
            'native': 0.0,
            'small_aggregates': 0.0,
            'large_aggregates': 0.0,
        }

        self._sort_percentage(data)
        self._calculate()
        self._normalize()

    def _sort_percentage(self, data: list[dict]):
        prev_row_index = None

        for values in data:
            if values['row'] != prev_row_index:
                self.row_count += 1
                prev_row_index = values['row']

            if AUTOLYSIS_LOWER_LIMIT_SIZE < values['diameter'] <= AUTOLYSIS_UPPER_LIMIT_SIZE:
                self.percentages['autolysis'].append(values['percentage'])

            elif NATIVE_LOWER_LIMIT_SIZE < values['diameter'] <= NATIVE_UPPER_LIMIT_SIZE:
                self.percentages['native'].append(values['percentage'])

            elif SMALL_AGGREGATES_LOWER_LIMIT_SIZE < values['diameter'] <= SMALL_AGGREGATES_UPPER_LIMIT_SIZE:
                self.percentages['small_aggregates'].append(values['percentage'])

            elif LARGE_AGGREGATES_LOWER_LIMIT_SIZE < values['diameter'] <= LARGE_AGGREGATES_UPPER_LIMIT_SIZE:
                self.percentages['large_aggregates'].append(values['percentage'])

            elif EXCLUSION_LOWER_LIMIT < values['diameter'] <= EXCLUSION_UPPER_LIMIT:
                logger.log_exclusion(values)

    def _calculate(self) -> None:
        for key in self.percentages:
            if self.row_count != 0:
                percentage = round(sum(self.percentages[key]) / self.row_count, DECIMAL_PLACES)
                self.calculations[key] = percentage
            else:
                logger.log_empty_y_label_values(self.y_label_value)

    def _normalize(self) -> None:
        calculations = list(self.calculations.values())
        summ = sum(calculations)

        if summ < 100:
            delta = 100 - summ
            max_value = max(calculations)

            for key, value in self.calculations.items():
                if value == max_value:
                    self.calculations[key] = max_value + delta
        elif summ > 100:
            raise RuntimeError('Summ percentage cannot exceed 100')

    def get_y_label_value(self):
        return self.y_label_value

    def get_autolysis(self):
        return self.calculations['autolysis']

    def get_native(self):
        return self.calculations['native']

    def get_small_aggregates(self):
        return self.calculations['small_aggregates']

    def get_large_aggregates(self):
        return self.calculations['large_aggregates']
