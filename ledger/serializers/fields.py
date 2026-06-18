from rest_framework import serializers
drom decimal import Decimal, InvalidOperation


class MoneyField(serializers.Field):
    """
    A custom field that stores value as USD deciaml 
    Api representations displays that converted to taka 
    it accepts a static conversion rate of 1 USD = 120 Taka
    """
    
    EXCHANGE_RATE = Decimal('120')

    def to_representation(self, value):
        # Convert the value from USD to Taka for API representation
        try:
            decimal_value = Decimal(value)
            taka_value = decimal_value * self.EXCHANGE_RATE
            return str(taka_value)
        except (InvalidOperation, TypeError):
            raise serializers.ValidationError("Invalid value for MoneyField. Must be a number.")
        
    def to_internal_value(self, data):
        # Convert the value from Taka to USD for internal storage
        try:
            decimal_value = Decimal(data)
            usd_value = decimal_value / self.EXCHANGE_RATE
            return str(usd_value)
        except (InvalidOperation, TypeError):
            raise serializers.ValidationError("Invalid value for MoneyField. Must be a number.")
        
    

class MaskedCardField(serializers.Field):
    """
    A custom field that masks credit card numbers for API representation.
    It displays only the first and last 4 digits of the card number, masking the rest with asterisks.
    """
    
    def to_representation(self, value):
        # Mask the credit card number for API representation
        if not isinstance(value, str) or len(value) < 4:
            raise serializers.ValidationError("Invalid value for MaskedCardField. Must be a string with at least 4 characters.")
        
        masked_value = value[:4] + '*' * (len(value) - 8) + value[-4:]
        return masked_value
    
    def to_internal_value(self, data):
        # Store the full credit card number internally
        if not isinstance(data, str) or len(data) < 4:
            raise serializers.ValidationError("Invalid value for MaskedCardField. Must be a string with at least 4 characters.")
        
        return data