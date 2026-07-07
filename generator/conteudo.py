# -*- coding: utf-8 -*-
"""Monta a story completa da apostila (une partes 1 e 2)."""

from conteudo_p1 import (
    sumario, glossario, aula1, aula2, aula3, aula4, aula5,
)
from conteudo_p2 import (
    aula6, aula7, aula8, aula9, exercicio_final,
)


def build_story():
    import gerar_apostila as ga
    story = []
    # Troca do template da capa para o template do corpo antes de sair da capa
    story.append(ga.NextPageTemplate("body"))
    story.append(ga.PageBreak())
    story += sumario()
    story += glossario()
    story += aula1()
    story += aula2()
    story += aula3()
    story += aula4()
    story += aula5()
    story += aula6()
    story += aula7()
    story += aula8()
    story += aula9()
    story += exercicio_final()
    return story
