from django.shortcuts import redirect
from django.contrib import messages


def perfil_required(*perfis):

    def decorator(view_func):

        def wrapper(request, *args, **kwargs):

            if not request.user.is_authenticated:

                return redirect('login')

            if not hasattr(request.user, 'perfil'):

                messages.error(
                    request,
                    'Usuário sem perfil definido.'
                )

                return redirect('dashboard')

            if request.user.perfil.tipo_usuario not in perfis:

                messages.error(
                    request,
                    'Você não possui permissão para acessar esta área.'
                )

                return redirect('dashboard')

            return view_func(
                request,
                *args,
                **kwargs
            )

        return wrapper

    return decorator