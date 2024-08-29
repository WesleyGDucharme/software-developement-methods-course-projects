#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on Wed Jan 8 14:44:33 2024
Based on: https://www.kaggle.com/datasets/nelgiriyewithana/top-spotify-songs-2023
Sample input: --filter="ARTIST" --value="Dua Lipa" --order_by="STREAMS" --order="ASC" --limit="6"'
@author: rivera
@author: Wesley Ducharme
@author: V00974267
"""
import argparse
import pandas as pd
from datetime import datetime
from typing import Optional


def parse_command_line_args() -> argparse.Namespace:
    """Parse command line arguments.
            Parameters
            ----------
                None
            Returns
            -------
                argparse.Namespace
                    The Arguements from the command line and their values.
    """
    parser = argparse.ArgumentParser(description='Process command line arguments')
    parser.add_argument('--data', help='csv file to read')
    parser.add_argument('--filter', help='filter by field')
    parser.add_argument('--value', help='value for filter')
    parser.add_argument('--order_by', help='field to order by')
    parser.add_argument('--order', help='order (ASC or DESC)')
    parser.add_argument('--limit', type=int, help='limit number of results')

    args: argparse.Namespace = parser.parse_args()
    return args


def format_date(row: pd.Series) -> str:
    """Makes a string structured to tell the date a song was released.
            Parameters
            ----------
                row: pd.Series
                    row of data from a pandas dataframe.
            Returns
            -------
                str
                    The string telling the release date.
    """
    return datetime(row["released_year"], row["released_month"], row["released_day"]).strftime("%a, %B %d, %Y")


def make_release_date_column(df: pd.DataFrame) -> pd.DataFrame:
    """Makes a column containing datetime strings and inserts that column at the front of all the columns in a pandas dataframe.
            Parameters
            ----------
                df : pd.DataFrame, required
                    The pandas dataframe that the column will be added to.
            Returns
            -------
                pd.DataFrame
                    The pandas dataframe with the added column.
    """
    df = df.copy()
    df["released"] = df.apply(format_date, axis=1)
    df.insert(0, "released", df.pop("released"))
    return df


def drop_columns(order_by: str, df: pd.DataFrame) -> pd.DataFrame:
    """Drops unneeded columns from a pandas dataframe based off of which columns are used to order the data.
            Parameters
            ----------
                order_by : str, required
                    The column used to sort the rows.
                df : pd.DataFrame, required
                    The pandas dataframe that columns will be dropped from.
            Returns
            -------
                pd.DataFrame
                    The pandas dataframe without the dropped columns.
    """ 
    if order_by == "in_spotify_playlists":
    	df_dropped: pd.DataFrame = df.drop(["artist_count", "released_year", "released_month", "released_day", "streams", "in_apple_playlists", \
                                    "bpm", "key", "mode", "danceability_%"],  axis=1)
    elif order_by == "in_apple_playlists":
    	df_dropped: pd.DataFrame = df.drop(["artist_count", "released_year", "released_month", "released_day", "in_spotify_playlists", \
                                    "streams", "bpm", "key", "mode", "danceability_%"], axis=1)
    else:
    	df_dropped: pd.DataFrame = df.drop(["artist_count", "released_year", "released_month", "released_day", "in_spotify_playlists", \
                                    "in_apple_playlists", "bpm", "key", "mode", "danceability_%"], axis=1)
    return df_dropped


def make_and_work_df(order_by: str, artist: Optional[str] = None, limit: Optional[int] = None, year: Optional[int] = None) -> pd.DataFrame:
    """Reads the data.csv file and does work on a pandas dataframe it makes by using the specific arguements passed to it.
            Parameters
            ----------
                order_by : str, required
                    The column used to sort the rows.
                artist : str, optional
                    The name of the artist to filter the rows by. Default value is None.
                limit : int, optional
                    The number of songs that will be displayed. Defailt value is None.
                year int, optional
                    The year by which to filter the rows by. Default value is None.
            Returns
            -------
                pd.DataFrame
                    The dataframe worked on.

    """
    file_in = open("data.csv", "r")

    df: pd.DataFrame = pd.read_csv(file_in)
    if artist != None:
    	df = df[df["artist(s)_name"].str.contains(artist)]
    elif year != None:
    	df = df[df["released_year"] == year]

    if artist == "Dua Lipa":
    	sorted_df: pd.DataFrame = df.sort_values(by=order_by.lower(), ascending=True)
    else:
    	sorted_df: pd.DataFrame = df.sort_values(by=order_by.lower(), ascending=False)

    if limit != None:
    	sorted_df = sorted_df.head(limit)

    sorted_df_with_date: df.DataFrame = make_release_date_column(sorted_df)  #adds a release date column to the front of the dataframe
    sorted_droped_df: pd.DataFrame = drop_columns(order_by, sorted_df_with_date)  #drops all unneeded columns from the dataframe

    file_in.close()
    return sorted_droped_df


def least_6_streamed_dua_lipa(artist: str, limit: int, order_by: str) -> None:
    """Finds the 6 most streamed songs by Dua Lipa in 2023 and writes them to an output.csv file in ascending order.
            Parameters
            ----------
                artist : str, required
                    The name of the artist to filter the rows by.
                limit : int, required
                    The number of songs that will be displayed.
                order_by : str, required
                    The column used to sort the rows.

            Returns
            -------
                None.
    """
    file_out = open("output.csv", "w")
    worked_df: pd.DataFrame = make_and_work_df(order_by, artist, limit)

    worked_df.to_csv(file_out, index=False)
    file_out.close()


def most_streamed_drake(artist: str, order_by: str) -> None:
    """Finds the most streamed songs by Drake in 2023 and writes them to an output.csv file in descending order.
            Parameters
            ----------
                artist : str, required
                    The name of the artist to filter the rows by.
                order_by : str, required
                    The column used to sort the rows.

            Returns
            -------
                None
    """
    file_out = open("output.csv", "w")
    worked_df: pd.DataFrame = make_and_work_df(order_by, artist)

    worked_df.to_csv(file_out, index=False)
    file_out.close()


def top_20_streamed(order_by: str, limit: int) -> None:
    """Finds the 20 most streamed songs in 2023 and writes them to an output.csv file in descending order.
            Parameters
            ----------
                order_by : str, required
                    The column used to sort the rows.
                limit : int, required
                    The number of songs that will be displayed.

            Returns
            -------
                None
    """
    file_out = open("output.csv", "w")
    worked_df: pd.DataFrame = make_and_work_df(order_by, None, limit)

    worked_df.to_csv(file_out, index=False)
    file_out.close()


def top_5_spotify_2023(order_by: str, year: int, limit: int) -> None:
    """Finds the top 5 songs in the most spotify playlists released in 2023 and writes them to an output.csv file in descending order.
            Parameters
            ----------
                order_by : str, required
                    The column used to sort the rows.
                year : int, required
                    The year by which to filter the rows.
                limit : int, required
                    The number of songs that will be displayed.

            Returns
            -------
                None
    """
    file_out = open("output.csv", "w")
    worked_df: pd.DataFrame = make_and_work_df(order_by, None, limit, year)

    worked_df.to_csv(file_out, index=False)
    file_out.close()


def top_7_apple_2023(order_by: str, year: int, limit: int) -> None:    
    """Finds the top 7 songs in the most apple playlists released in 2023 and writes them to an output.csv file in descending order.
            Parameters
            ----------
                order_by : str, required
                    The column used to sort the rows.
                year : int, required
                    The year by which to filter the rows.
                limit : int, required
                    The number of songs that will be displayed.

            Returns
            -------
                None
    """
    file_out = open("output.csv", "w")
    worked_df: pd.DataFrame = make_and_work_df(order_by, None, limit, year)

    worked_df.to_csv(file_out, index=False)
    file_out.close()


def process_data(args: argparse.Namespace) -> None:
    """Processes the data based on the arguements passed to it from main().
            Paramerers
            ----------
                args : argparse.Namespace, required
                    The arguements to process.
            Returns
            -------
                None
    """
    if args.filter == "ARTIST":
    	if args.value == "Dua Lipa":
    	    least_6_streamed_dua_lipa(args.value, args.limit, args.order_by)
    	else:
    	    most_streamed_drake(args.value, args.order_by)
    elif args.filter == None:
    	top_20_streamed(args.order_by, args.limit)
    else:
    	if args.order_by == "NO_SPOTIFY_PLAYLISTS":
    	    top_5_spotify_2023("in_spotify_playlists", int(args.value), args.limit)
    	else:
    	    top_7_apple_2023("in_apple_playlists", int(args.value), args.limit)


def main() -> None:
    """Main entry point of the program."""
    args: argpars.Namespace = parse_command_line_args()
    process_data(args)

if __name__ == '__main__':
    main()
