from django import forms

from .models import Procedimento


# =========================================
# FORM PROCEDIMENTO
# =========================================

class ProcedimentoForm(forms.ModelForm):

    class Meta:

        model = Procedimento

        fields = [

            'nome',
            'categoria',
            'tipo',
            'cor',
            'icone',
            'posicao_icone',
            'ativo',
            'ordem'

        ]

        widgets = {

            'nome': forms.TextInput(

                attrs={

                    'class': 'form-control'

                }

            ),

            'categoria': forms.Select(

                attrs={

                    'class': 'form-select'

                }

            ),

            'tipo': forms.Select(

                attrs={

                    'class': 'form-select'

                }

            ),

            'cor': forms.TextInput(

                attrs={

                    'class': 'form-control',

                    'type': 'color'

                }

            ),

            'icone': forms.TextInput(

                attrs={

                    'class': 'form-control',

                    'placeholder': 'Ex: canal.png'

                }

            ),

            'posicao_icone': forms.Select(

                attrs={

                    'class': 'form-select'

                }

            ),

            'ativo': forms.CheckboxInput(

                attrs={

                    'class': 'form-check-input'

                }

            ),

            'ordem': forms.NumberInput(

                attrs={

                    'class': 'form-control'

                }

            )

        }