import cProfile
import os
import random
import typing


class ProfilerConfig:
    def __init__(self, enabled: bool, profiles_root_dir='profiles'):
        self.enabled = enabled
        self.profiles_root_dir = profiles_root_dir
        os.makedirs(self.profiles_root_dir, exist_ok=True)

    def get_path_for(self, profile_name: typing.Optional[str] = None) -> str:
        if not profile_name:
            profile_name = self._get_random_name()
        return f'{self.profiles_root_dir}/{profile_name}.prof'

    @staticmethod
    def _get_random_name() -> str:
        return hex(random.getrandbits(16 * 4))


def maybe_profile(profile_naming_function):
    def wrapped_decorator(f):
        def wrapped_func(self, *args, **kwargs):
            if self.profiler_config.enabled:
                profile_name = profile_naming_function(self, *args, **kwargs)
                profile_path = self.profiler_config.get_path_for(profile_name)
                with cProfile.Profile() as pr:
                    f(self, *args, **kwargs)
                    pr.dump_stats(profile_path)
                    print(f'debug: wrote profiler output to {profile_path}')
            else:
                f(self, *args, **kwargs)

        return wrapped_func

    return wrapped_decorator
