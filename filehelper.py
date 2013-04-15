import csv


def tickets_from_file(filename):
    """read tickets from file filename and return dict of tickets"""
    def array_to_ticket_dict(array):
        """modify array to ticket-like dictionary"""
        return {
            'jira_id': array[1],
            'jira_name': array[2],
            'properties': {
                'Author': 'svitko',
                'Iteration - Scheduled': '(Current Iteration)',
                'Status': 'Ready to be Played',
                'Story Tree - Project': 606,
                'Estimate': array[3]
            }
        }

    if filename is not None:
        tickets_file = open(filename, 'r')
        data = csv.reader(tickets_file, delimiter=',')

        table = [array_to_ticket_dict(row) for row in data]
        return table

    else:
        raise RuntimeError("Filename can't be None")


def main():
    tickets = tickets_from_file("tickets.csv")

    for ticket in tickets:
        print(ticket)

if __name__ == "__main__":
    main()
