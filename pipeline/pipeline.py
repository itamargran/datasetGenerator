import json
import os

import pandas as pd


class GenerateAnalysisDataset:
    COLUMN_NAME = "patterns_dict"

    def __init__(self, path_to_csv: str, pattern_name: str) -> None:
        self.raw_df = pd.read_csv(path_to_csv)
        self.pattern_name = pattern_name
        self.create_file_for_analysis()

    @staticmethod
    def convert_str_to_dict(text: str) -> dict:
        text = text.replace("'", "\"")
        try:
            return json.loads(text)
        except (json.JSONDecodeError, AssertionError):
            return {}

    def convert_text_column_to_dict(self, col_name: str) -> None:
        col = [self.convert_str_to_dict(item) for item in self.raw_df[col_name]]
        self.raw_df[col_name] = col

    def isolate_relevant_data_in_separate_column(self) -> None:
        self.raw_df["just_" + self.pattern_name] = (
            [item.get(self.pattern_name, "") for item in self.raw_df[self.COLUMN_NAME]]
        )

    def raw_data_preprocessing(self) -> None:
        self.convert_text_column_to_dict(self.COLUMN_NAME)
        self.isolate_relevant_data_in_separate_column()

    def create_new_dataframe(self) -> pd.DataFrame:
        self.raw_data_preprocessing()

        new_df_data = {col_name: [] for col_name in self.raw_df.columns}
        new_df_data.update({self.pattern_name: []})

        for _, row in self.raw_df.iterrows():
            for item in row["just_" + self.pattern_name]:
                if item:
                    new_df_data[self.pattern_name].append(item)
                    for column in self.raw_df.columns:
                        new_df_data[column].append(row[column])

        return pd.DataFrame.from_dict(new_df_data)

    def create_file_for_analysis(self):
        df = self.create_new_dataframe()
        df.to_csv(os.path.join(os.getcwd(), self.pattern_name + "_dataset.csv"))
