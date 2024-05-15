import os
import sys
import csv
import inspect

class DjangoGenerator:
    def __init__(self, csv_file, output_dir):
        self.output_dir = output_dir

        json = build_json_from_csv(csv_file)

        for object_type in json:

            title_field = False
            model_name = create_object_name(object_type)

            # Generate model class and write to file
            # model_file_path = self.generate_model_class(model_name, json[object_type])

            # Generate serializer class and write to file
            serializer_file_path = self.generate_serializer_class(model_name)

            # Generate viewset class and write to file
#           viewset_file_path = self.generate_viewset(model_name, serializer_class, output_dir)

    @staticmethod
    def generate_model_class(class_name, fields):
        for field in fields:
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

        fields = {"header": models.CharField(max_length=255)}

        model_class = type('DynamicModel', (models.Model,), fields)

        # Convert model class to string
        model_class_as_string = '\n'.join([line for line in model_class.__str__().split('\n') if line.strip()])

        # Write model class to file
        model_file_path = os.path.join(output_dir, 'dynamic_model.py')
        with open(model_file_path, 'w') as model_file:
            model_file.write(model_class_as_string)

        return model_file_path

    def generate_serializer_class(self, model_class):
        class DynamicSerializer(serializers.ModelSerializer):
            class Meta:
                model = model_class
                fields = '__all__'

        class_name = f"{model_class}Serializer"
        RenamedClass = type(class_name, DynamicSerializer.__bases__, dict(DynamicSerializer.__dict__))
        class_source_code = '\n'.join(inspect.getsourcelines(RenamedClass)[0])

        serializer_file_path = os.path.join(self.output_dir, f'{class_name}.py')

        with open(serializer_file_path, 'w', encoding='utf-8') as file:
            file.write(class_source_code)

        return serializer_file_path

    @staticmethod
    def generate_viewset(model_class, serializer_class_param, output_dir):
        class DynamicViewSet(viewsets.ModelViewSet):
            queryset = model_class.objects.all()
            serializer_class = serializer_class_param

        viewset_class_as_string = viewsets.serialize(DynamicViewSet, indent=4)

        # Write viewset class to file
        viewset_file_path = os.path.join(output_dir, 'dynamic_viewset.py')
        with open(viewset_file_path, 'w') as viewset_file:
            viewset_file.write(viewset_class_as_string)

        return viewset_file_path



if __name__ == "__main__":
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'nod_backend.settings.dev')

    from django.core.management import execute_from_command_line
    from django.db import models
    from rest_framework import serializers, viewsets
    from scaffolding.utils import create_machine_name, create_object_name, addArgs, infer_field_type, build_json_from_csv
    from django.conf import settings

    execute_from_command_line(sys.argv)
#    settings.configure()

    DjangoGenerator("./scaffolding/object-fields.csv", './scaffolding')
