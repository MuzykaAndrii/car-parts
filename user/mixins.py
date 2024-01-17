from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin


class MyLoginRequiredMixin(LoginRequiredMixin):
    login_url = 'user:login'


class AdminRequiredMixin(MyLoginRequiredMixin, UserPassesTestMixin):
    def test_func(self) -> bool:
        return self.request.user.is_superuser