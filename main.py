import argparse as ap
from pathlib import Path
import csv
import random
import json

# Names of allowed months, days, and times based on the task description.
ALLOWED_MONTHS = [
    "styczeń", "luty", "marzec", "kwiecień", "maj", "czerwiec", "lipiec",
    "sierpień", "wrzesień", "październik", "listopad", "grudzień"
]
ALLOWED_DAYS = ["pn", "wt", "śr", "czw", "pt", "sb", "nd"]
ALLOWED_TIMES = ["r", "w"]

MODELS = ["A", "B", "C"]
DATA_RANGE = 1000

def validate_day_range(day_range):
    bounds = day_range.split("-")

    if len(bounds) == 1:
        if bounds[0] not in ALLOWED_DAYS:
            raise ap.ArgumentTypeError(f"Błąd. Nie rozpoznano dnia '{bounds[0]}'.")

    elif len(bounds) == 2:
        start, end = bounds[0], bounds[1]

        if start not in ALLOWED_DAYS:
            raise ap.ArgumentTypeError(f"Błąd. Nie rozpoznano dnia początkowego '{start}'.")

        if end not in ALLOWED_DAYS:
            raise ap.ArgumentTypeError(f"Błąd. Nie rozpoznano dnia końcowego '{end}'.")

        if ALLOWED_DAYS.index(start) > ALLOWED_DAYS.index(end):
            raise ap.ArgumentTypeError(f"Błąd. Nieprawidłowa kolejność dni w zakresie '{day_range}'.")

    else:
        raise ap.ArgumentTypeError(f"Błąd. Nieprawidłowy format zakresu '{day_range}'.")

    return day_range

def build_parser():
    parser = ap.ArgumentParser(
        description="Skrypt do tworzenia i odczytu plików CSV i JSON w strukturze katalogów.",
        epilog="Przykładowe użycie: python main.py -m styczeń luty -d pn-wt pt -p r w -t"
    )

    parser.add_argument(
        "-m", "--miesiące",
        dest="months",
        nargs="+",
        required=True,
        choices=ALLOWED_MONTHS,
        metavar="MIESIĄCE",
        help=f"Lista miesięcy. "
             f"Dozwolone miesiące: {', '.join(ALLOWED_MONTHS)}."
    )

    parser.add_argument(
        "-d", "--dni",
        dest="days",
        nargs="+",
        required=True,
        type=validate_day_range,
        metavar="DNI",
        help=f"Lista zakresów dni (np. pn-śr, pt). "
             f"Dozwolone dni: {', '.join(ALLOWED_DAYS)}."
    )

    parser.add_argument(
        "-p", "--pory",
        dest="times",
        nargs="*",
        default=[],
        choices=ALLOWED_TIMES,
        metavar="PORA",
        help="Pory dnia odpowiednio dla kolejnych dni: 'r' (rano) lub 'w' (wieczór). "
             "Domyślną wartością jest 'r'."
    )

    parser.add_argument(
        "-t", "--twórz",
        dest="create_mode",
        action="store_true",
        help="Tryb tworzenia plików. "
             "Brak tej flagi oznacza domyślnie tryb odczytu."
    )

    parser.add_argument(
        "-f", "--format",
        dest="file_format",
        choices=["csv", "json"],
        default="csv",
        help="Format plików: csv lub json. Domyślnie csv."
    )

    return parser

def validate_args(args, parser):
    if len(args.months) != len(args.days):
        parser.error(
            f"Błąd. Liczba miesięcy ({len(args.months)}) "
            f"musi być równa liczbie zakresów dni ({len(args.days)})."
        )

    total_days = sum(len(split_range(day_range)) for day_range in args.days)

    if len(args.times) > total_days:
        parser.error(
            f"Błąd. Podano {len(args.times)} pór dnia, "
            f"ale wybrano tylko {total_days} dni."
        )

DAY_NAMES = {
    "pn": "poniedziałek",
    "wt": "wtorek",
    "śr": "środa",
    "czw": "czwartek",
    "pt": "piątek",
    "sb": "sobota",
    "nd": "niedziela"
}

TIME_NAMES = {
    "r": "rano",
    "w": "wieczorem"
}

def split_range(lst):
    if "-" not in lst:
        return [lst]

    start, end = lst.split("-")
    startId = ALLOWED_DAYS.index(start)
    endId = ALLOWED_DAYS.index(end)
    return ALLOWED_DAYS[startId:endId + 1]

def expand_day(d):
    return DAY_NAMES[d]

def expand_time(t):
    return TIME_NAMES[t]

def generate_paths(months, days, times):
    paths = []
    timeId = 0

    for month, day_range in zip(months, days):
        expDays = split_range(day_range)
        for day in expDays:
            time = times[timeId] if timeId < len(times) else "r"
            timeId += 1

            day = expand_day(day)
            time = expand_time(time)

            path = Path(month, day, time)
            paths.append(path)

    return paths

def generate_file_paths(paths, file_format="csv"):
    file_paths = []
    for path in paths:
        file_paths.append(path / ("Dane." + file_format))
    return file_paths

def create_directories(paths):
    for path in paths:
        path.mkdir(parents=True, exist_ok=True)

def generate_data(paths):
    for path in paths:
        generated_data = [
            MODELS[random.randint(0, len(MODELS)-1)],
            random.randint(0, DATA_RANGE),
            str(random.randint(0, DATA_RANGE)) + "s"
        ]

        with open(path, 'w', encoding='utf-8', newline='') as file:
            csvwriter = csv.writer(file, delimiter=';')
            csvwriter.writerow(["Model", " Wynik", " Czas", ""])
            csvwriter.writerow([
                generated_data[0] + " ",
                " " + str(generated_data[1]) + " ",
                " " + generated_data[2],
                ""
            ])

def generate_json_data(paths):
    for path in paths:
        generated_data = {
            "Model": MODELS[random.randint(0, len(MODELS) - 1)],
            "Wynik": random.randint(0, DATA_RANGE),
            "Czas": str(random.randint(0, DATA_RANGE)) + "s"
        }

        with open(path, 'w', encoding='utf-8') as file:
            json.dump(generated_data, file)

def read_data(file_paths, model):
    model_sum = 0

    for path in file_paths:
        if not path.exists():
            print(f"Błąd. Plik {path} nie istnieje")
            return None

        with open(path, 'r', encoding='utf-8', newline='') as file:
            csvreader = csv.DictReader(file, delimiter=';', skipinitialspace=True)

            for row in csvreader:
                if row["Model"].strip() == model:
                    model_sum += int(row["Czas"].strip().split("s")[0])

    return model_sum

def read_json_data(file_paths, model):
    model_sum = 0

    for path in file_paths:
        if not path.exists():
            print(f"Błąd. Plik {path} nie istnieje")
            return None

        with open(path, 'r', encoding='utf-8') as file:
            data = json.load(file)

            if data["Model"] == model:
                model_sum += int(data["Czas"].split("s")[0])

    return model_sum

def main():
    parser = build_parser()
    args = parser.parse_args()

    validate_args(args, parser)

    paths = generate_paths(args.months, args.days, args.times)
    file_paths = generate_file_paths(paths, args.file_format)

    if args.create_mode:
        create_directories(paths)

        if args.file_format == "csv":
            generate_data(file_paths)
        else:
            generate_json_data(file_paths)

    else:
        if args.file_format == "csv":
            response = read_data(file_paths, "A")
        else:
            response = read_json_data(file_paths, "A")

        if response is not None:
            print(str(response) + "s")

if __name__ == '__main__':
    main()