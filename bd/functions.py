def get_json_file_frazes(frazes):
    frazes_json = []

    for fraze in frazes:
        frazes_json.append(
            {
                'id': fraze[0],
                'action': fraze[1],
                'text_fraze': fraze[2]
            }
        )

    return frazes_json
