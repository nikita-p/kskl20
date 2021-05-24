# Tutorials

## Содержание
1. <a name="mcgpj">MCGPJ моделирование со своим формфактором каона</a>
1. <a name="points">Получить список точек по сезонам</a>
1. <a name="mctruth">Добавить в MC генераторные параметры частиц</a>
1. <a name="actual_condor">Актуальные файлы для кондора</a>


## [MCGPJ моделирование со своим формфактором каона](#mcgpj)
Алгоритм:

1. Установить `cmd3sim` на компьютер согласно алгоритму на [сайте](https://cmd.inp.nsk.su/wiki/bin/view/CMD3/Cmd3SimFirstRun)
1. Иинциализировать переменные `cmd3sim` двумя командами:
    1. `source /sl/cmd3/cc7-64/Cmd3Sim/bin/env64.csh`
    1. `source config/env64.sh`
1. Теперь с программой можно работать по алгоритму с этой [страницы](https://cmd.inp.nsk.su/wiki/bin/view/CMD3/Cmd3SimRun)
1. Чтобы вставить свой формфактор в моделирование нужно изменить файл `generator/radcor/src/TKnFormFactor.C` и видимо снова сделать `make`

## [Получить список точек по сезонам](#points)
Алгоритм:

1. Выполнить `source /sl/cmd3/cc7-64/Cmd3Off/tune.cmd3_runs_scripts.sh`
1. Выполнить `listoffdata.py --listpoints`

## [Добавить в MC генераторные параметры частиц](#mctruth)
Алгоритм:

1. В конфиг моделирования в блок "McTruth" добавить конфигурацию генераторных частиц, которые нужно сохранить.
Подробнее на этой [странице](https://cmd.inp.nsk.su/wiki/pub/CMD3/Cmd3SimConfig/mctruth.xml)
2. В конфиге в разделе "Persistency" установить "MCTruth" 1

## [Актуальные файлы для condor](#actual_condor)
Посмотреть в 

* `/sl/cmd3/cc7-64/CmdPackages-svn/jobopts/`
* `/spoolA/ignatov/cmdsoft/condor/`