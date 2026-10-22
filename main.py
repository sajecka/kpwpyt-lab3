import argparse as ap
import sys

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


def main():
    parser = build_parser()
    args = parser.parse_args()

    validate_args(args, parser)

    # Testowanie
    # print(f"Miesiące: {args.months}")
    # print(f"Dni: {args.days}")
    # print(f"Pory: {args.times}")
    # print(f"Tworzenie: {args.create_mode}")

if __name__ == '__main__':
    main()