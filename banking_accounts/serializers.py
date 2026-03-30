from rest_framework import serializers


class TransactionSerializer(serializers.Serializer):
    operation = serializers.ChoiceField(choices=["credit", "debit"])
    account_id = serializers.IntegerField
    amount = serializers.DecimalField(max_digits=12, decimal_places=2)

    def validate_amount(self, value):
        if value <= 0:
            raise serializers.ValidationError("Amount must be greater than 0")
        return value


class TransferSerializer(serializers.Serializer):
    from_account = serializers.IntegerField()
    to_account = serializers.IntegerField()
    amount = serializers.DecimalField(max_digits=12, decimal_places=2)

    def validate(self, data):
        if data["from_account"] == data["to_account"]:
            raise serializers.ValidationError("Cannot transfer to same account")
        if data["amount"] <= 0:
            raise serializers.ValidationError("Amount must be greater than 0")
        return data
