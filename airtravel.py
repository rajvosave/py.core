"""Model for aircraftfllights."""


class Flight:

    def __init__(self, number, aircraft):
        if not number[:2].isalpha():
            raise ValueError(f"No airline code in '{number}'")

        if not number[:2].isupper():
            raise ValueError(f"Invalid airline code '{number}'")

        if not (number[2:].isdigit() and int(number[2:]) <= 9999):
            raise ValueError(f"Invalid route number '{number}'")

        self._number = number
        self._aircraft = aircraft
        rows, seats = self._aircraft.seating_plan()
        self._seating = [None] + [{letter: None for letter in seats}for _ in rows]

    def number(self):
        return self._number

    def airline(self):
        return self._number[:2]

    def aircraft_model(self):
        return self._aircraft.model()

    def allocate_seats(self, seat, passanger):
        """Allocate a seat to passanger
        Args:
            seat: A seat designator as "callable"
            passanger: passanger name
        """
        row, letter = self._parse_seat(seat)

        if self._seating[row][letter] is not None:
            raise ValueError(f"Seat {seat} allready taken")

        self._seating[row][letter] = passanger

    def _parse_seat(self, seat):
        rows, seat_letters = self._aircraft.seating_plan()

        letter = seat[-1]
        if letter not in seat_letters:
            raise ValueError(f"Invalid seat letter {letter}")
        row_text = seat[:-1]
        try:
            row = int(row_text)
        except ValueError:
            raise ValueError(f"Invalid seat row {row_text}")

        if row not in rows:
            raise ValueError(f"Invalid row number {row}")

        return row, letter

    def relocate_passanger(self, from_seat, to_seat):
        from_row, from_letter = self._parse_seat(from_seat)
        if self._seating[from_row][from_letter] is None:
            raise ValueError(f"No passanger to move from seat {from_seat}")

        to_row, to_letter = self._parse_seat(to_seat)
        if self._seating[to_row][to_letter] is not None:
            raise ValueError(f"Selected seat {to_seat} is already taken")

        self._seating[to_row][to_letter] = self._seating[from_row][from_letter]
        self._seating[from_row][from_letter] = None

    def num_available_seats(self):
        return sum(sum(1 for s in row.values() if s is None)
                  for row in self._seating
                  if row is not None)

    def make_boarding_card(self, console_card_printer):
        for passanger, seats in sorted(self._passanger_seats()):
            console_card_printer(passanger, seats, self._number, self.aircraft_model())

    def _passanger_seats(self):
        row_numbers, seat_letters = self._aircraft.seating_plan()
        for row in row_numbers:
            for letter in seat_letters:
                passanger = self._seating[row][letter]
                if passanger is not None:
                    yield (passanger, f"{row}{letter}")


class Aircraft:
    def __init__(self, registration, model, num_rows, num_seats_per_row):
        self._registraton = registration
        self._model = model
        self._num_rows = num_rows
        self._num_seats_per_row = num_seats_per_row

    def registration(self):
        return self._registraton

    def model(self):
        return self._model

    def seating_plan(self):
        return (range(1, self._num_rows + 1),
                "ABCDEFGJK"[:self._num_seats_per_row])


def console_card_printer(passanger, seat, flight_number, aircraft):
    output = f"| Name: {passanger}"       \
             f"  Flight: {flight_number}" \
             f"  Seat: {seat}"            \
             f"  Aircraft: {aircraft}"    \
            "|"
    banner = "+" + "-" * (len(output) - 2) + "+"
    border = "|" + "-" * (len(output) - 2) + "|"
    lines = [banner, border, output, banner, border]
    card = "\n".join(lines)
    print(card)
    print()


def make_flight():
    f = Flight("CO888", Aircraft("G-EUPT", "Propelerac", 
                                 num_rows=22, num_seats_per_row=6))
    f.allocate_seats("1A", "vedran")
    f.allocate_seats("1B", "Tanja")
    f.allocate_seats("15F", "Marko")
    return f
