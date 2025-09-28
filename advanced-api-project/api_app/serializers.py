from rest_framework import serializers
from .models import Author, Book
from datetime import datetime

class BookSerializer(serializers.ModelSerializer):
    """Serializer for Book model with custom validation."""
    class Meta:
        model = Book
        fields = '__all__'

    def validate_publication_year(self, value):
        """Ensure publication year is not in the future."""
        current_year = datetime.now().year
        if value > current_year:
            raise serializers.ValidationError("Publication year cannot be in the future.")
        return value


class AuthorSerializer(serializers.ModelSerializer):
    """Serializer for Author model with nested books."""
    books = BookSerializer(many=True, read_only=True)

    class Meta:
        model = Author
        fields = ['name', 'books']
