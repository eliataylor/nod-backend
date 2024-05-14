import csv
import json
import re


def inject_generated_code(output_file_path, code):
    with open(output_file_path, 'r', encoding='utf-8') as file:
        html = file.read()

    start = html.find("###OBJECT-ACTIONS-MODELS-STARTS###") + len("###OBJECT-ACTIONS-MODELS-STARTS###")
    end = html.find("###OBJECT-ACTIONS-MODELS-ENDS###")

    start_html = html[:start]
    end_html = html[end:]
    html = start_html + code + end_html

    with open(output_file_path, 'w', encoding='utf-8') as file:
        file.write(html)

    print('HTML file has been generated successfully.')

def build_json_from_csv(csv_file):
    # Initialize an empty dictionary to store JSON object
    json_data = {}

    # Open the CSV file
    with open(csv_file, 'r') as csvfile:
        # Create a CSV reader object
        reader = csv.DictReader(csvfile)

        cur_type = None
        # Iterate over each row in the CSV
        for row in reader:
            # Extract the type from the row
            obj_type = row['TYPES']
            if obj_type is not None and obj_type != '':
                cur_type = obj_type

            if row['Field Label'] is None or row['Field Label'] == '':
                continue

            if cur_type is None:
                continue

            # Remove 'Type' from the row since we don't need it in the JSON object
            del row['TYPES']

            # Check if the type already exists in the JSON object
            if cur_type in json_data:
                # Append the row to the existing array
                json_data[cur_type].append(row)
            else:
                # Create a new array with the row as its first element
                json_data[cur_type] = [row]

    return json_data

def build_all_models(json):
    model_code = ""
    # model_code = "from django.db import models\n"
    # if 'user' not in json and 'User' not in json and 'Users' not in json:
        # model_code += f"from django.contrib.auth.models import User\n"

    for object_type in json:
        title_field = False
        model_name = create_object_name(object_type)
        model_code += f"\nclass {model_name}(SuperModel):\n"

        for field in json[object_type]:
            field_type = field['Field Type']
            field_name = field['Field Name']
            if field_name is None or field_name == '':
                field_name = create_machine_name(field['Field Label'])

            if field_name == 'title':
                title_field = field_name
            elif field_name == 'name':
                title_field = field_name

            if field_type is None:
                field_type = 'text'
            model_type = infer_field_type(field_type, field)
            if field['Required'].strip() == '' or int(field['Required']) < 1:
                model_type = addArgs(model_type, ['blank=True', 'null=True'])
            if field['Default'].strip() != '':
                model_type = addArgs(model_type, [f"default={field['Default']}"])

            model_code += f"    {field_name} = {model_type}\n"

#        if title_field is not None:
#            model_code += "\n   def __str__(self):"
#            model_code += f"\n      return self.{title_field}\n"

        model_code += f"admin.site.register({model_name})\n"


    return model_code


def addArgs(target, new_args):
    # Split the target string into function name and arguments
    func_name, args_str = target.split('(')

    # Remove trailing parenthesis from args string and split the arguments
    args = args_str.rstrip(')').split(',')

    # Add non-empty new arguments to the existing arguments list
    args.extend(new_args)

    # Filter out empty strings from new_args
    args = [arg for arg in args if arg != '']

    # Combine function name and modified arguments
    if len(args) == 1:  # If there is only one argument, no need for a comma
        modified_target = f"{func_name}({args[0]})"
    else:
        modified_target = f"{func_name}({', '.join(args)})"

    return modified_target


def infer_field_type(field_type, field):
    field_type = field_type.lower()
    if field_type == "text":
        return "models.CharField(max_length=255)"  # Adjust max_length as needed
    elif field_type == "textarea":
        return "models.TextField()"
    elif field_type == "integer":
        return "models.IntegerField()"
    elif field_type == "decimal":
        return "models.DecimalField(max_digits=10, decimal_places=2)"  # Adjust precision as needed
    elif field_type == "date":
        return "models.DateField()"
    elif field_type == "url":
        return "models.URLField()"
    elif field_type == "id":
        return "models.AutoField(primary_key=True)"
    elif field_type == "boolean":
        return "models.BooleanField()"
    elif field_type == "image":
        return "models.ImageField()"
    elif field_type == "video":
        return "models.FileField(upload_to='videos/')"
    elif field_type == "media":
        return "models.FileField(upload_to='media/')"
    elif field_type == "list_of_strings":
        return "models.JSONField()"  # Store both as JSON array
    elif field_type == "json":
        return "models.JSONField()"  # Store both as JSON array
    elif field_type == "enum":
        return f"models.CharField(max_length=20, choices=MealTimes.choices)"
    elif field_type == "vocabulary reference" or field_type == field_type == "type reference":
        # return "models.ManyToManyField()"
        # return "models.OneToOneField()"
        model_name = create_object_name(field['Relationship'])
        return f"models.ForeignKey('{model_name}', on_delete=models.CASCADE)"
    elif field_type == "address":
        return "models.CharField(max_length=2555)"  # Adjust max_length as needed
    else:
        return "models.TextField()"

def create_object_name(label):
    return re.sub(r'[^a-zA-Z0-9\s]', '', label).replace(' ', '')

def create_machine_name(label, lower=True):
    # Remove special characters and spaces, replace them with underscores
    machine_name = re.sub(r'[^a-zA-Z0-9\s]', '', label).strip().replace(' ', '_')
    if lower is True:
        machine_name = machine_name.lower()
    return machine_name

# Example usage
csv_file = "object-fields.csv"

model_json = build_json_from_csv(csv_file)
f = open("models.json", "w")
f.write(json.dumps(model_json, indent=2))
f.close()

model_code = build_all_models(model_json)
inject_generated_code('../nod_backend/models.py', model_code)

f = open("models.py", "w")
f.write(model_code)
f.close()

# You can save the generated code to a file named 'models.py' in your app directory
