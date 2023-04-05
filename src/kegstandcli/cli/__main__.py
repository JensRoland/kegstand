import os
import click


from kegstandcli.cli.new import new
from kegstandcli.cli.build import build
from kegstandcli.cli.deploy import deploy
from kegstandcli.cli.teardown import teardown

ALIASES = {
    'init': new,
    'up': deploy,
    'party': deploy,
    'down': teardown
}

CONFIG_FILE_NAMES = ['kegstand.toml', '.kegstand', 'pyproject.toml']

class AliasedGroup(click.Group):
    def get_command(self, ctx, cmd_name):
        try:
            cmd_name = ALIASES[cmd_name].name
        except KeyError:
            pass
        return super().get_command(ctx, cmd_name)


# We pass the project directory to all subcommands via the context
# so they can use it to find the kegstand.toml file
@click.group(cls=AliasedGroup)
@click.option('--config', help='Path to Kegstand configuration file.')
@click.option('--verbose', is_flag=True, default=False, help='Show verbose output')
@click.pass_context
def kegstandcli(ctx, config, verbose):  # ANSI art generated with https://dom111.github.io/image-to-ansi/
    """\b
\033[49m                        \033[38;5;232;48;5;52m▄\033[38;5;234;48;5;52m▄\033[38;5;232;49m▄▄▄\033[38;5;236;48;5;52m▄\033[38;5;245;48;5;233m▄\033[38;5;252;48;5;232m▄\033[38;5;230;48;5;233m▄\033[38;5;230;48;5;234m▄\033[38;5;230;48;5;233m▄\033[38;5;253;48;5;232m▄\033[38;5;248;48;5;232m▄\033[38;5;59;48;5;52m▄\033[38;5;233;49m▄\033[38;5;232;49m▄\033[49m     \033[38;5;52;49m▄\033[49m       \033[m
\033[49m                        \033[49;38;5;52m▀\033[38;5;52;48;5;236m▄\033[38;5;237;48;5;188m▄\033[38;5;254;48;5;252m▄\033[38;5;230;48;5;253m▄\033[38;5;230;48;5;230m▄\033[38;5;222;48;5;223m▄\033[38;5;222;48;5;222m▄▄▄▄▄▄\033[38;5;222;48;5;229m▄\033[38;5;222;48;5;253m▄\033[38;5;229;48;5;242m▄\033[38;5;249;48;5;232m▄\033[38;5;234;48;5;52m▄\033[38;5;52;49m▄\033[49m  \033[38;5;52;48;5;233m▄\033[38;5;239;48;5;232m▄\033[38;5;234;48;5;52m▄\033[38;5;52;49m▄\033[49m    \033[m
\033[49m                        \033[38;5;52;49m▄\033[38;5;232;49m▄\033[38;5;240;48;5;52m▄\033[38;5;144;48;5;236m▄\033[38;5;101;48;5;186m▄\033[38;5;180;48;5;222m▄\033[38;5;222;48;5;222m▄▄▄▄▄▄\033[48;5;222m \033[38;5;222;48;5;222m▄▄▄▄\033[38;5;222;48;5;252m▄\033[38;5;187;48;5;235m▄\033[38;5;235;48;5;52m▄\033[38;5;52;49m▄\033[38;5;236;48;5;233m▄\033[38;5;254;48;5;102m▄\033[38;5;221;48;5;143m▄\033[38;5;237;48;5;232m▄\033[38;5;52;49m▄\033[49m   \033[m
\033[49m                       \033[38;5;233;48;5;52m▄\033[38;5;250;48;5;234m▄\033[38;5;222;48;5;249m▄\033[38;5;185;48;5;229m▄\033[38;5;221;48;5;221m▄\033[38;5;179;48;5;221m▄\033[38;5;179;48;5;137m▄\033[38;5;137;48;5;180m▄\033[38;5;143;48;5;222m▄\033[38;5;222;48;5;222m▄▄▄\033[48;5;222m \033[38;5;222;48;5;222m▄▄▄▄▄▄▄\033[38;5;249;48;5;144m▄\033[38;5;230;48;5;238m▄\033[38;5;222;48;5;253m▄\033[38;5;222;48;5;222m▄\033[38;5;179;48;5;221m▄\033[38;5;137;48;5;95m▄\033[38;5;232;48;5;233m▄\033[49m   \033[m
\033[49m                      \033[38;5;234;48;5;233m▄\033[38;5;187;48;5;243m▄\033[38;5;221;48;5;222m▄\033[38;5;221;48;5;215m▄\033[38;5;221;48;5;179m▄\033[38;5;222;48;5;179m▄▄\033[38;5;179;48;5;137m▄\033[38;5;101;48;5;143m▄\033[38;5;143;48;5;101m▄\033[38;5;180;48;5;101m▄\033[38;5;101;48;5;222m▄\033[38;5;222;48;5;222m▄▄▄\033[38;5;179;48;5;186m▄\033[38;5;186;48;5;222m▄\033[38;5;222;48;5;222m▄▄▄▄▄▄▄\033[38;5;221;48;5;222m▄\033[38;5;143;48;5;179m▄\033[38;5;101;48;5;137m▄\033[38;5;232;48;5;232m▄\033[49m   \033[m
\033[49m                     \033[38;5;232;48;5;52m▄\033[38;5;250;48;5;242m▄\033[38;5;221;48;5;221m▄\033[38;5;222;48;5;221m▄\033[38;5;222;48;5;222m▄▄▄\033[38;5;137;48;5;221m▄\033[38;5;223;48;5;101m▄\033[38;5;223;48;5;223m▄\033[38;5;223;48;5;222m▄\033[38;5;222;48;5;222m▄\033[38;5;222;48;5;216m▄\033[38;5;222;48;5;101m▄\033[38;5;95;48;5;186m▄\033[38;5;137;48;5;222m▄\033[38;5;222;48;5;222m▄\033[38;5;222;48;5;179m▄\033[38;5;179;48;5;186m▄\033[38;5;180;48;5;222m▄\033[38;5;222;48;5;222m▄▄▄\033[38;5;221;48;5;222m▄\033[38;5;143;48;5;221m▄\033[38;5;179;48;5;137m▄\033[38;5;179;48;5;221m▄\033[38;5;143;48;5;95m▄\033[38;5;236;48;5;233m▄\033[49m   \033[m
\033[49m                    \033[38;5;52;49m▄\033[38;5;235;48;5;235m▄\033[38;5;235;48;5;179m▄\033[38;5;221;48;5;179m▄\033[38;5;222;48;5;222m▄▄▄▄\033[38;5;246;48;5;101m▄\033[38;5;138;48;5;223m▄\033[38;5;223;48;5;223m▄▄▄▄\033[38;5;180;48;5;222m▄\033[38;5;144;48;5;137m▄\033[38;5;95;48;5;180m▄\033[38;5;238;48;5;95m▄\033[38;5;234;48;5;137m▄\033[38;5;240;48;5;221m▄\033[38;5;137;48;5;221m▄\033[38;5;137;48;5;179m▄\033[38;5;179;48;5;221m▄\033[38;5;221;48;5;179m▄▄\033[38;5;179;48;5;179m▄\033[38;5;101;48;5;215m▄\033[38;5;179;48;5;101m▄\033[38;5;221;48;5;221m▄\033[38;5;236;48;5;237m▄\033[38;5;52;48;5;233m▄\033[49m  \033[m
\033[49m                    \033[49;38;5;52m▀\033[38;5;52;48;5;232m▄\033[38;5;232;48;5;234m▄\033[38;5;179;48;5;221m▄\033[38;5;222;48;5;222m▄\033[38;5;221;48;5;222m▄\033[38;5;222;48;5;222m▄\033[38;5;236;48;5;222m▄\033[38;5;235;48;5;144m▄\033[38;5;238;48;5;223m▄\033[38;5;238;48;5;144m▄\033[38;5;223;48;5;223m▄▄\033[38;5;144;48;5;138m▄\033[38;5;181;48;5;238m▄\033[38;5;188;48;5;102m▄\033[38;5;242;48;5;242m▄\033[38;5;239;48;5;235m▄\033[38;5;95;48;5;59m▄\033[38;5;221;48;5;221m▄▄\033[38;5;179;48;5;179m▄\033[38;5;221;48;5;137m▄▄\033[38;5;179;48;5;101m▄\033[38;5;143;48;5;95m▄\033[38;5;179;48;5;179m▄\033[38;5;221;48;5;221m▄\033[38;5;137;48;5;179m▄\033[38;5;232;48;5;233m▄\033[49m   \033[m
\033[49m                      \033[49;38;5;52m▀\033[38;5;233;48;5;237m▄\033[38;5;95;48;5;222m▄\033[38;5;222;48;5;179m▄\033[38;5;179;48;5;179m▄\033[38;5;179;48;5;221m▄\033[38;5;137;48;5;137m▄\033[38;5;243;48;5;102m▄\033[38;5;243;48;5;238m▄\033[38;5;180;48;5;223m▄\033[38;5;223;48;5;223m▄\033[48;5;223m \033[38;5;223;48;5;223m▄\033[38;5;255;48;5;251m▄\033[38;5;181;48;5;242m▄\033[38;5;180;48;5;242m▄\033[38;5;137;48;5;137m▄\033[38;5;221;48;5;221m▄\033[38;5;137;48;5;221m▄\033[38;5;179;48;5;137m▄\033[38;5;179;48;5;221m▄\033[38;5;238;48;5;221m▄\033[38;5;245;48;5;101m▄\033[38;5;223;48;5;187m▄\033[38;5;223;48;5;138m▄\033[38;5;180;48;5;137m▄\033[38;5;234;48;5;235m▄\033[49;38;5;52m▀\033[49m   \033[m
\033[49m                        \033[38;5;232;48;5;233m▄\033[38;5;221;48;5;222m▄\033[38;5;222;48;5;222m▄\033[38;5;101;48;5;143m▄\033[38;5;223;48;5;181m▄\033[38;5;223;48;5;223m▄▄\033[38;5;181;48;5;144m▄\033[38;5;247;48;5;223m▄\033[38;5;246;48;5;223m▄\033[38;5;223;48;5;223m▄▄\033[38;5;181;48;5;187m▄\033[38;5;180;48;5;95m▄\033[38;5;180;48;5;137m▄\033[38;5;137;48;5;101m▄\033[38;5;95;48;5;179m▄\033[38;5;131;48;5;179m▄\033[38;5;101;48;5;236m▄\033[38;5;187;48;5;59m▄\033[38;5;240;48;5;101m▄\033[38;5;237;48;5;144m▄\033[38;5;101;48;5;223m▄\033[38;5;241;48;5;223m▄\033[38;5;243;48;5;138m▄\033[38;5;234;48;5;233m▄\033[49m   \033[m
\033[49m                       \033[38;5;232;48;5;52m▄\033[38;5;232;48;5;237m▄\033[38;5;232;48;5;101m▄\033[38;5;232;48;5;235m▄\033[38;5;235;48;5;233m▄\033[38;5;239;48;5;144m▄\033[38;5;234;48;5;223m▄\033[38;5;180;48;5;223m▄\033[38;5;138;48;5;245m▄\033[38;5;132;48;5;248m▄\033[38;5;132;48;5;240m▄\033[38;5;223;48;5;223m▄▄▄\033[38;5;222;48;5;223m▄\033[38;5;137;48;5;216m▄\033[38;5;131;48;5;89m▄\033[38;5;167;48;5;167m▄▄\033[38;5;236;48;5;95m▄\033[38;5;137;48;5;180m▄\033[38;5;221;48;5;95m▄\033[38;5;179;48;5;234m▄\033[38;5;95;48;5;233m▄\033[38;5;236;48;5;233m▄\033[38;5;234;48;5;233m▄\033[38;5;233;48;5;234m▄\033[38;5;232;48;5;233m▄\033[49m  \033[m
\033[49m                    \033[38;5;233;49m▄\033[38;5;235;48;5;52m▄\033[38;5;8;48;5;232m▄\033[38;5;246;48;5;233m▄\033[38;5;102;48;5;233m▄\033[38;5;102;48;5;232m▄\033[38;5;245;48;5;232m▄\033[38;5;240;48;5;243m▄\033[38;5;235;48;5;236m▄\033[38;5;232;48;5;234m▄\033[38;5;234;48;5;237m▄\033[38;5;236;48;5;180m▄\033[38;5;236;48;5;132m▄\033[38;5;239;48;5;138m▄\033[38;5;101;48;5;187m▄\033[38;5;137;48;5;180m▄\033[38;5;239;48;5;101m▄\033[38;5;1;48;5;238m▄\033[38;5;89;48;5;235m▄\033[38;5;167;48;5;167m▄▄\033[38;5;125;48;5;167m▄\033[38;5;233;48;5;234m▄\033[38;5;179;48;5;179m▄\033[38;5;221;48;5;221m▄▄▄\033[38;5;179;48;5;221m▄\033[38;5;238;48;5;179m▄\033[38;5;232;48;5;234m▄\033[49m   \033[m
\033[49m                   \033[38;5;233;49m▄\033[38;5;59;48;5;233m▄\033[38;5;247;48;5;102m▄\033[38;5;168;48;5;248m▄\033[38;5;167;48;5;174m▄\033[38;5;167;48;5;175m▄\033[38;5;167;48;5;102m▄\033[38;5;174;48;5;239m▄\033[38;5;239;48;5;239m▄\033[38;5;233;48;5;233m▄\033[38;5;232;48;5;232m▄\033[38;5;233;48;5;52m▄\033[38;5;234;48;5;125m▄\033[38;5;180;48;5;137m▄\033[38;5;223;48;5;222m▄▄\033[38;5;138;48;5;222m▄\033[38;5;235;48;5;239m▄\033[38;5;234;48;5;1m▄\033[38;5;125;48;5;125m▄\033[38;5;52;48;5;125m▄\033[38;5;233;48;5;125m▄▄\033[38;5;233;48;5;233m▄\033[38;5;58;48;5;179m▄\033[38;5;179;48;5;221m▄\033[38;5;179;48;5;137m▄\033[38;5;237;48;5;137m▄\033[38;5;233;48;5;101m▄\033[38;5;232;48;5;233m▄\033[49m    \033[m
\033[49m                  \033[38;5;232;48;5;52m▄\033[38;5;241;48;5;235m▄\033[38;5;174;48;5;246m▄\033[38;5;174;48;5;168m▄\033[38;5;251;48;5;174m▄\033[38;5;174;48;5;167m▄\033[38;5;175;48;5;167m▄\033[38;5;167;48;5;167m▄▄\033[38;5;125;48;5;131m▄\033[38;5;52;48;5;232m▄\033[38;5;0;48;5;232m▄\033[38;5;232;48;5;233m▄\033[38;5;236;48;5;236m▄▄\033[38;5;236;48;5;239m▄\033[38;5;236;48;5;236m▄▄▄\033[38;5;233;48;5;234m▄\033[38;5;233;48;5;52m▄\033[49;38;5;232m▀\033[49;38;5;233m▀\033[49m  \033[38;5;232;48;5;236m▄\033[38;5;237;48;5;137m▄\033[38;5;239;48;5;95m▄\033[38;5;52;48;5;233m▄\033[49m      \033[m
\033[49m                 \033[38;5;233;48;5;233m▄\033[38;5;145;48;5;239m▄\033[38;5;238;48;5;8m▄\033[38;5;95;48;5;167m▄\033[38;5;167;48;5;175m▄\033[38;5;167;48;5;224m▄\033[38;5;174;48;5;15m▄\033[38;5;254;48;5;188m▄\033[38;5;255;48;5;167m▄\033[38;5;131;48;5;125m▄\033[38;5;125;48;5;125m▄\033[38;5;232;48;5;52m▄\033[38;5;232;48;5;232m▄▄\033[38;5;233;48;5;233m▄\033[38;5;236;48;5;236m▄▄▄\033[38;5;236;48;5;235m▄\033[38;5;235;48;5;234m▄\033[38;5;232;48;5;232m▄\033[49m     \033[38;5;233;48;5;52m▄\033[38;5;232;48;5;235m▄\033[38;5;232;48;5;234m▄\033[49m       \033[m
\033[49m               \033[38;5;52;49m▄\033[38;5;235;48;5;233m▄\033[38;5;248;48;5;243m▄\033[38;5;239;48;5;242m▄\033[38;5;245;48;5;8m▄\033[38;5;238;48;5;239m▄\033[38;5;237;48;5;237m▄\033[38;5;235;48;5;131m▄\033[38;5;1;48;5;125m▄\033[38;5;125;48;5;125m▄\033[38;5;125;48;5;174m▄\033[38;5;52;48;5;125m▄\033[38;5;0;48;5;233m▄\033[38;5;239;48;5;232m▄\033[38;5;175;48;5;233m▄\033[38;5;167;48;5;242m▄\033[38;5;167;48;5;138m▄\033[38;5;167;48;5;89m▄\033[38;5;167;48;5;236m▄▄▄▄\033[38;5;131;48;5;233m▄\033[38;5;236;48;5;232m▄\033[38;5;233;49m▄▄\033[49m  \033[49;38;5;52m▀\033[49;38;5;232m▀\033[49m        \033[m
\033[49m               \033[38;5;232;48;5;233m▄\033[38;5;238;48;5;245m▄\033[38;5;235;48;5;239m▄\033[38;5;237;48;5;240m▄\033[38;5;238;48;5;238m▄▄\033[38;5;236;48;5;237m▄\033[38;5;234;48;5;235m▄\033[38;5;234;48;5;234m▄\033[38;5;232;48;5;233m▄\033[38;5;0;48;5;232m▄\033[38;5;239;48;5;0m▄\033[38;5;174;48;5;242m▄\033[38;5;167;48;5;174m▄\033[48;5;167m \033[38;5;167;48;5;167m▄\033[48;5;167m   \033[38;5;167;48;5;167m▄▄▄\033[48;5;167m \033[38;5;167;48;5;167m▄\033[38;5;167;48;5;131m▄\033[38;5;167;48;5;52m▄\033[38;5;131;48;5;232m▄\033[38;5;232;48;5;233m▄\033[38;5;233;49m▄\033[49m         \033[m
\033[49m               \033[49;38;5;52m▀\033[38;5;233;48;5;232m▄\033[38;5;232;48;5;232m▄\033[38;5;233;48;5;232m▄\033[38;5;233;48;5;234m▄\033[38;5;232;48;5;237m▄\033[38;5;234;48;5;234m▄▄\033[38;5;0;48;5;233m▄\033[38;5;0;48;5;0m▄\033[38;5;232;48;5;0m▄\033[38;5;232;48;5;243m▄\033[38;5;235;48;5;167m▄\033[38;5;89;48;5;167m▄\033[38;5;167;48;5;167m▄▄▄\033[48;5;167m \033[38;5;167;48;5;167m▄▄▄▄▄▄\033[38;5;89;48;5;167m▄\033[38;5;233;48;5;131m▄\033[38;5;232;48;5;233m▄\033[49;38;5;232m▀\033[49m          \033[m
\033[49m                 \033[49;38;5;233m▀\033[38;5;52;48;5;232m▄\033[38;5;232;48;5;232m▄\033[38;5;0;48;5;0m▄▄\033[38;5;0;48;5;232m▄\033[38;5;0;48;5;0m▄\033[38;5;232;48;5;232m▄\033[49;38;5;52m▀\033[49;38;5;233m▀\033[38;5;232;48;5;232m▄\033[38;5;234;48;5;234m▄\033[38;5;234;48;5;235m▄\033[38;5;234;48;5;131m▄\033[38;5;125;48;5;167m▄\033[38;5;167;48;5;167m▄▄▄▄\033[38;5;89;48;5;167m▄\033[38;5;234;48;5;131m▄\033[38;5;233;48;5;235m▄\033[38;5;233;48;5;233m▄\033[49;38;5;232m▀\033[49m            \033[m
\033[49m                    \033[49;38;5;233m▀\033[49;38;5;232m▀▀▀\033[49m  \033[38;5;52;49m▄\033[38;5;239;48;5;232m▄\033[38;5;239;48;5;234m▄\033[38;5;234;48;5;234m▄▄\033[38;5;232;48;5;233m▄\033[38;5;233;48;5;234m▄\033[38;5;233;48;5;236m▄▄\033[38;5;52;48;5;234m▄\033[38;5;237;48;5;233m▄\033[38;5;187;48;5;234m▄\033[38;5;101;48;5;233m▄\033[38;5;233;48;5;233m▄\033[49m             \033[m
\033[49m                          \033[38;5;233;48;5;52m▄\033[38;5;8;48;5;242m▄\033[38;5;223;48;5;223m▄\033[38;5;222;48;5;144m▄\033[38;5;239;48;5;240m▄\033[38;5;233;48;5;232m▄\033[49m    \033[38;5;52;48;5;233m▄\033[38;5;237;48;5;101m▄\033[38;5;236;48;5;95m▄\033[38;5;233;48;5;233m▄\033[38;5;233;49m▄\033[49m            \033[m
\033[49m                          \033[38;5;232;48;5;233m▄\033[38;5;249;48;5;247m▄\033[38;5;223;48;5;223m▄\033[38;5;137;48;5;216m▄\033[38;5;232;48;5;233m▄\033[49m      \033[38;5;233;48;5;237m▄\033[38;5;234;48;5;238m▄\033[38;5;232;48;5;234m▄\033[49;38;5;233m▀\033[49m            \033[m
\033[49m                         \033[38;5;232;48;5;52m▄\033[38;5;245;48;5;239m▄\033[38;5;236;48;5;236m▄\033[38;5;235;48;5;238m▄\033[38;5;232;48;5;235m▄\033[38;5;52;48;5;52m▄\033[49m                      \033[m
\033[49m                         \033[38;5;233;48;5;233m▄\033[38;5;8;48;5;138m▄\033[38;5;235;48;5;236m▄\033[38;5;233;48;5;234m▄\033[38;5;232;48;5;232m▄\033[49m                       \033[m
\033[38;5;167m██   ██ ███████  ██████  ███████ ████████  █████  ███    ██ ██████             
██  ██  ██      ██       ██         ██    ██   ██ ████   ██ ██   ██            
█████   █████   ██   ███ ███████    ██    ███████ ██ ██  ██ ██   ██            
██  ██  ██      ██    ██      ██    ██    ██   ██ ██  ██ ██ ██   ██            
██   ██ ███████  ██████  ███████    ██    ██   ██ ██   ████ ██████             
===================================================================            
The Developer's Toolbelt For Accelerating Mean-Time-To-Party on AWS\033[m"""
    # Locate the correct Kegstand configuration file
    if config is None:
        for name in CONFIG_FILE_NAMES:
            if os.path.exists(name):
                config = name
                break

    if not os.path.exists(config):
        raise click.ClickException(f'Configuration file not found: {config}')

    project_dir = os.path.abspath(os.path.dirname(config))
    ctx.obj = {
        'config': os.path.abspath(config),
        'project_dir': project_dir,
        'verbose': verbose
    }

for command in [new, build, deploy, teardown]:
    kegstandcli.add_command(command)

if __name__ == '__main__':
    kegstandcli(obj={})
