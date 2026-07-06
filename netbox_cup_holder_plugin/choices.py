from django.utils.translation import gettext_lazy as _
from utilities.choices import ChoiceSet


class CupholderMountFaceChoices(ChoiceSet):

    FACE_FRONT = 'front'
    FACE_LEFT = 'left'
    FACE_RIGHT = 'right'

    CHOICES = (
        (FACE_FRONT, _('Front')),
        (FACE_LEFT, _('Left side')),
        (FACE_RIGHT, _('Right side')),
    )


class CupholderSizeChoices(ChoiceSet):

    SIZE_XS = 'xs'
    SIZE_S = 's'
    SIZE_M = 'm'
    SIZE_L = 'l'
    SIZE_XL = 'xl'
    SIZE_XXL = 'xxl'

    CHOICES = (
        (SIZE_XS, _('XS')),
        (SIZE_S, _('S')),
        (SIZE_M, _('M')),
        (SIZE_L, _('L')),
        (SIZE_XL, _('XL')),
        (SIZE_XXL, _('XXL')),
    )
