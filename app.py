import datetime
import os

from rich.console import Console
from rich.padding import Padding
from rich.text import Text

import database

console = Console()

os.system("cls")


menu = """Select one of the following options:

    1) [green]New entry.[/]
    2) List entries.
    3) Get entries by year.
    4) Get entries by month and year.
    5) Get entry by entry date.
    6) Search entries.
    7) [bold red]Exit.[/]

Your selection: """


welcome = Text("Welcome to the BEST Journal app in the universe")
welcome.stylize("bold cyan blink", 15, 31)


console.print(Padding(welcome, 2))
database.create_tables()


def print_entry_list(entries):
    os.system("cls")
    console.print("[cyan]--- Entries ---[/] \n")
    if not entries:
        console.print("[red]No entries to print.[/]")
        return

    for entry in entries:
        entry_date = datetime.datetime.fromtimestamp(entry[3])
        human_date = entry_date.strftime("%A - %B %d, %Y - %I:%M %p")
        console.print(f"{human_date}")

        console.print(Padding(f"[bold]{entry[1]}[/]", (1)))

        console.print(entry[2], width=80, overflow="fold", justify="full")
        console.print("\n")  # Add a newline for spacing between entries


def prompt_get_entries_by_year():
    while True:
        entries_year = console.input(
            "What year's entries would you like to see? Enter '[red]exit[/]' to go back [italic]YYYY[/]: "
        )
        if entries_year.lower() == "exit":
            os.system("cls")
            return []
        try:
            year_int = int(entries_year)
            entries = database.get_entries_by_year(year_int)
            if entries:
                return entries
            else:
                os.system("cls")
                console.print(
                    f"[red]No entries[/] found for the year [cyan]{entries_year}[/]. Please try another year. \n"
                )
        except ValueError:
            os.system("cls")
            console.print(
                f"'[cyan]{entries_year}[/]' is not a valid year. Please enter a valid year or type '[red]exit[/]' to go back. \n"
            )


def prompt_get_entries_by_month_and_year():
    while True:
        entries_month = console.input(
            "What month's entries would you like to see? Enter 1-12 or '[red]exit[/]' to go back: "
        )
        if entries_month.lower() == "exit":
            os.system("cls")
            return []

        if not entries_month.isdigit() or not 1 <= int(entries_month) <= 12:
            console.print(
                "[red]Invalid month.[/] Please enter a number between [cyan]1 and 12[/]. \n"
            )
            continue

        month_int = int(entries_month)

        # Year input loop
        while True:
            entries_year = console.input(
                "What year's entries would you like to see? Enter '[red]exit[/]' to go back [italic]YYYY[/]: "
            )
            if entries_year.lower() == "exit":
                os.system("cls")
                return []

            if not entries_year.isdigit():
                console.print("[red]Invalid input.[/] Please enter a valid year. \n")
                continue

            year_int = int(entries_year)
            break

        entries = database.get_entries_by_month_and_year(month_int, year_int)
        if entries:
            return entries
        else:
            os.system("cls")
            console.print(
                f"[red]No entries found[/] for [cyan]{entries_month}/{entries_year}[/]. Please try another month/year. \n"
            )


def prompt_get_entry_by_date():
    while True:
        entry_date_input = console.input(
            "Enter the date for the entries you'd like to see (YYYY-MM-DD) or '[red]exit[/]' to go back: "
        )
        if entry_date_input.lower() == "exit":
            os.system("cls")

            return []

        try:
            year, month, day = map(int, entry_date_input.split("-"))
            entry_date = datetime.date(year, month, day)
            entries = database.get_entry_by_date(entry_date)
            if entries:
                return entries
            else:
                os.system("cls")
                console.print(
                    f"[red]No entries found[/] for [cyan]{entry_date}[/]. Please try another date. \n"
                )
        except ValueError:
            os.system("cls")
            console.print(
                "[red]Invalid date format or invalid date.[/] Please enter a valid date in YYYY-MM-DD format. \n"
            )


def prompt_search_entries():
    search_term = input("Enter search term: ")
    return database.search_entries(search_term)


while True:
    user_input = console.input(menu)
    if user_input == "7":
        os.system("cls")
        console.print("[bold magenta]See ya next time!![/] \n")
        break
    elif user_input == "1":
        os.system("cls")
        entry_title = input("Enter a title: ")
        os.system("cls")
        console.print(f"Title: [cyan]{entry_title}[/]")
        entry_content = console.input("[bold]Entry: [/]")
        database.add_entry(entry_title, entry_content)
        os.system("cls")
        console.print("[green]Entered Successfully[/]\n")
    elif user_input == "2":
        entries = database.get_entries()
        print_entry_list(entries)
    elif user_input == "3":
        os.system("cls")
        entries = prompt_get_entries_by_year()
        if entries:
            print_entry_list(entries)
    elif user_input == "4":
        os.system("cls")
        entries = prompt_get_entries_by_month_and_year()
        if entries:
            print_entry_list(entries)
    elif user_input == "5":
        os.system("cls")
        entry = prompt_get_entry_by_date()
        if entry:
            print_entry_list(entry)
    elif user_input == "6":
        os.system("cls")
        entries = prompt_search_entries()
        if entries:
            print_entry_list(entries)
        else:
            os.system("cls")
            console.print("[red]Found no entries[/] for that search term! \n")
    else:
        os.system("cls")
        console.print("[red]Invalid input[/], please try again!")
