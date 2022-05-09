def loop_through_authors(func):
    def modify_authors(*args):
        updated_authors = args[0]
        authors_to_be_modified = args[1]
        if len(authors_to_be_modified) > len(updated_authors):
            index = len(updated_authors)
            while index < len(authors_to_be_modified):
                arguments = [authors_to_be_modified[index]]
                if len(args) > 2:
                    arguments.append(args[2])

                func(arguments)
                index += 1

    return modify_authors
