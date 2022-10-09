import pymorphy2


def fix_morph(name, amount):
    """
    Корректирует название в зависимости от количества.
    '1 бутылка, 2 бутылки, 5 бутылок....'
    """

    morph = pymorphy2.MorphAnalyzer()
    return morph.parse(name)[0].make_agree_with_number(amount).word
