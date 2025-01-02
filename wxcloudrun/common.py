import enum


class SourceType(enum.Enum):
    def __str__(self):
        return self.value

    USER_CLOTHES = 1
    CLOTHES_STORE = 2


class ClothingCategory(enum.Enum):
    def __str__(self):
        return self.value

    tops = "内搭"
    bottoms = "下装"
    outerwear = "外套"
