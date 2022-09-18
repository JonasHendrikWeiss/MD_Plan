from Zuordnung import ChurchService
from Storage_Operations import data_storage
from docx import Document


def print_to_docx(data, path_template = "template_plan", name_output="plan" ):
    document = Document(str(path_template))
    if len(document.tables) == 1:  # checks if there is only one table else it generates a new table
        table = document.tables[0]
    else:
        table = document.add_table(1, 3)

    amount_services = len(data.list_services)
    for number in range(amount_services):
        service = data.list_services[number]
        table.cell(number, 0).text = service.date.strftime("%d.%m.%Y")
        table.cell(number, 1).text = service.time.strftime('%H:%M')
        text_abbreviations = " "  # A text to which all abbreviations of all MDs are added
        for amount in range(len(service.current_churchservers)):
            text_abbreviations = text_abbreviations + service.current_churchservers[amount].abbreviation
            table.cell(0, 3).text = text_abbreviations
    # Saves the document with the given name
    document.save(name_output)
