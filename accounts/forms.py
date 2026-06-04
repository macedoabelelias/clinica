from django import forms

from .models import (

    Procedimento,
    Orcamento,
    ItemOrcamento,
    Convenio

)


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
            'status',

            'icone',
            'arquivo_icone',

            'posicao_icone',

            'valor_particular',

            'tempo_estimado',
            'custo_clinico',

            'ativo',

        ]

        widgets = {

    'nome': forms.TextInput(

        attrs={

            'class': 'form-control shadow-sm'

        }

    ),

    'categoria': forms.Select(

        attrs={

            'class': 'form-select shadow-sm'

        }

    ),

    'tipo': forms.Select(

        attrs={

            'class': 'form-select shadow-sm'

        }

    ),

    'status': forms.Select(

        attrs={

            'class': 'form-select shadow-sm'

        }

    ),

    # ===== POSIÇÃO ÍCONE =====
    'posicao_icone': forms.Select(

        attrs={

            'class': 'form-select shadow-sm'

        }

    ),

    'icone': forms.TextInput(

        attrs={

            'class': 'form-control shadow-sm',

            'placeholder': 'Digite ou pesquise um ícone'

        }

    ),

    'valor_particular': forms.NumberInput(

        attrs={

            'class': 'form-control shadow-sm',

            'step': '0.01',

            'placeholder': 'Valor Particular'

        }

    ),

    'valor_convenio': forms.NumberInput(

        attrs={

            'class': 'form-control shadow-sm',

            'step': '0.01',

            'placeholder': 'Valor Convênio'

        }

    ),
    

    'tempo_estimado': forms.NumberInput(

        attrs={

            'class': 'form-control shadow-sm',

            'placeholder': 'Tempo em minutos'

        }

    ),

    'custo_clinico': forms.NumberInput(

        attrs={

            'class': 'form-control shadow-sm',

            'step': '0.01',

            'placeholder': 'Custo Clínico'

        }

    ),

    'ativo': forms.CheckboxInput(

        attrs={

            'class': 'form-check-input'

        }

    ),

    'ordem': forms.NumberInput(

        attrs={

            'class': 'form-control shadow-sm'

        }

    )

}


# =========================================
# ORÇAMENTO
# =========================================

class OrcamentoForm(forms.ModelForm):

    class Meta:

        model = Orcamento

        fields = [

            'desconto',
            'observacoes'

        ]

        widgets = {

            'desconto': forms.NumberInput(

                attrs={

                    'class': 'form-control',

                    'step': '0.01'

                }

            ),

            'observacoes': forms.Textarea(

                attrs={

                    'class': 'form-control',

                    'rows': 3

                }

            )

        }


# =========================================
# ITEM ORÇAMENTO
# =========================================

class ItemOrcamentoForm(forms.ModelForm):

    class Meta:

        model = ItemOrcamento

        fields = [

            'procedimento',
            'quantidade'

        ]

        widgets = {

            'procedimento': forms.Select(

                attrs={

                    'class': 'form-select rounded-3 shadow-sm'

                }

            ),

            'quantidade': forms.NumberInput(

                attrs={

                    'class': 'form-control rounded-3 shadow-sm',
                    'min': 1

                }

            )

        }
        
 # =========================================
# FORM CONVÊNIO
# =========================================

class ConvenioForm(forms.ModelForm):

    class Meta:

        model = Convenio

        fields = [

            'nome',
            'indice',
            'telefone',
            'observacoes',
            'ativo'

        ]

        widgets = {

            'nome': forms.TextInput(

                attrs={

                    'class': 'form-control shadow-sm'

                }

            ),

            'indice': forms.NumberInput(

                attrs={

                    'class': 'form-control shadow-sm',
                    'step': '0.01'

                }

            ),

            'telefone': forms.TextInput(

                attrs={

                    'class': 'form-control shadow-sm'

                }

            ),

            'observacoes': forms.Textarea(

                attrs={

                    'class': 'form-control shadow-sm',
                    'rows': 3

                }

            ),

            'ativo': forms.CheckboxInput(

                attrs={

                    'class': 'form-check-input'

                }

            )

        }       