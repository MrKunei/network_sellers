from rest_framework import serializers
from .models import Product, Seller


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'


class SellerSerializer(serializers.ModelSerializer):
    products = serializers.SlugRelatedField(many=True, slug_field='title', read_only=True)
    parent = serializers.SlugRelatedField(read_only=True, slug_field='name')
    employees = serializers.SlugRelatedField(read_only=True, slug_field='username')

    class Meta:
        model = Seller
        fields = '__all__'


class SellerCreateSerializer(serializers.ModelSerializer):
    products = serializers.SlugRelatedField(many=True,
                                            queryset=Product.objects.all(),
                                            slug_field='title', required=False)
    parent = serializers.SlugRelatedField(queryset=Seller.objects.all(),
                                          slug_field='name', required=False)

    def create(self, validated_data):
        lvl = validated_data['parent'].level
        if lvl < 5:
            self._prod = validated_data.pop('products')
            seller = Seller.objects.create(**validated_data)
            for p in self._prod:
                seller.products.add(p)
            seller.save()
            return seller
        else:
            raise AssertionError("Выбранный поставщик на максимальном уровне сети: 5")

    class Meta:
        model = Seller
        fields = "__all__"


class SellerUpdateSerializer(serializers.ModelSerializer):
    products = serializers.SlugRelatedField(many=True, slug_field='title',
                                            required=False,
                                            queryset=Product.objects.all())
    parent = serializers.SlugRelatedField(slug_field='name', required=False,
                                          queryset=Seller.objects.all())

    def save(self, **kwargs):
        lvl = self.validated_data['parent'].level
        if lvl < 5:
            seller = super().save(**kwargs)
            return seller
        else:
            raise AssertionError(
                "Выбранный поставщик на максимальном уровне сети: 5")

    class Meta:
        model = Seller
        exclude = ('debt',)