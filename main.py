import argparse as ap
import sys
from pathlib import Path

# Nazwy miesięcy/dni tygodnia/pór dnia jak w przykładzie z treści zadania.
ALLOWED_MONTHS = [
    "styczeń", "luty", "marzec", "kwiecień", "maj", "czerwiec", "lipiec",
    "sierpień", "wrzesień", "październik", "listopad", "grudzień"
]
ALLOWED_DAYS = ["pn", "wt", "śr", "czw", "pt", "sb", "nd"]
ALLOWED_TIMES = ["r", "w"]

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
        description="Skrypt do tworzenia i odczytu plików CSV w strukturze katalogów.",
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

    return parser

def validate_args(args, parser):
    if len(args.months) != len(args.days):
        parser.error(
            f"Błąd. Liczba miesięcy ({len(args.months)}) "
            f"musi być równa liczbie zakresów dni ({len(args.days)})."
        )

    total_days = sum(len(split_range(day_range)) for day_range in args.days)

    if (len(args.times) > total_days):
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

# Helper function for person 3
def generate_file_paths(paths):
    file_paths = []
    for path in paths:
        file_paths.append(path / "Dane.csv")
    return file_paths

def create_directories(paths):
    for path in paths:
        path.mkdir(parents=True, exist_ok=True)


def main():
    parser = build_parser()
    args = parser.parse_args()

    validate_args(args, parser)

    paths = generate_paths(args.months, args.days, args.times)

    if args.create_mode:
        create_directories(paths)

    file_paths = generate_file_paths(paths)

    for path in file_paths:
        print(path)

    # Testowanie
    # print(f"Miesiące: {args.months}")
    # print(f"Dni: {args.days}")
    # print(f"Pory: {args.times}")
    # print(f"Tworzenie: {args.create_mode}")

if __name__ == '__main__':
    main()