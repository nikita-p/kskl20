# Tutorials

## Содержание
1. <a name="mcgpj">MCGPJ моделирование со своим формфактором каона</a>


## [MCGPJ моделирование со своим формфактором каона](#mcgpj)
Алгоритм:

1. Установить `cmd3sim` на компьютер согласно алгоритму на [сайте](https://cmd.inp.nsk.su/wiki/bin/view/CMD3/Cmd3SimFirstRun)
1. Иинциализировать переменные `cmd3sim` двумя командами:
    1. `source /sl/cmd3/cc7-64/Cmd3Sim/bin/env64.csh`
    1. `source config/env64.sh`
1. Теперь с программой можно работать по алгоритму с этой [страницы](https://cmd.inp.nsk.su/wiki/bin/view/CMD3/Cmd3SimRun)
1. Чтобы вставить свой формфактор в моделирование нужно изменить файл `generator/radcor/src/TKnFormFactor.C` и видимо снова сделать `make`