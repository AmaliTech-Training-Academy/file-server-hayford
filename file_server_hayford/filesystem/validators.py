from django.core.exceptions import ValidationError

def file_size_validation(file):
    max_size =600
    if file.size > max_size *1024:
        raise ValidationError('file can\'t be larger than {0} kb'.format(max_size))