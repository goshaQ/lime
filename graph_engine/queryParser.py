from moz_sql_parser import parse
from pyparsing import ParseException
import json
from WrongStatement import WrongStatement

class Parser():
    def parse(self, query):
        try:
            self.__check_statement(query)
        except ParseException:
            print("Check your query. And RTFM.")
        except WrongStatement as e:
            print(e)

    def __check_statement(self, query):
        tokens = json.dumps(parse(query))
        tokens = json.loads(tokens)
        self.__check__select(tokens)
        return self.__process_where(tokens)

    def __check__select(self, tokens):
        if "select" in tokens:
            if "*" != tokens["select"]["value"]:
                raise WrongStatement("Check return values. And RTFM.")
    
    def __process_where(self, tokens):
        if "where" not in tokens:
            print("Return all values")
            self.__return_all()
        else:
            where_values = tokens["where"]
            for key in where_values.keys():
                if "eq" == key:
                    clause = where_values["eq"]
                    property_name = clause[0]
                    property_value = clause[1]["literal"]
                elif "and" == key:
                    clauses = where_values["and"]
                    names, values = self.__get_properties(clauses)

                elif "or" == key:
                    clauses = where_values["or"]
                    names, values = self.__get_properties(clauses)

    def __get_properties(self, clauses):
        first_clause = clauses[0]['eq']
        first_property_name = first_clause[0]
        first_property_value = first_clause[1]['literal']
        second_clause = clauses[1]['eq']
        second_property_name = second_clause[0]
        second_property_value = second_clause[1]['literal']

        return [first_property_name, second_property_name], [first_property_value, second_property_value]

    def __return_all(self):
        pass
        # Call function for getting all values


parser = Parser()
parser.parse("TEST *")
parser.parse("SELECT *")
parser.parse("SELECT name")
parser.parse("SELECT * FROM scene WHERE size='big'")
parser.parse("SELECT * FROM scene WHERE size='big' AND color='red'")
parser.parse("SELECT * FROM scene WHERE size='big' OR size='medium'")
        
