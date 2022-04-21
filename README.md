# 3d-reconstruction


## На всякий случай работа с сабмодулями

Для того чтобы склонировать проект с сабмодулями(т.е. этот)

```
git clone --recurse-submodules git@github.com:kadmus-dev/3d-reconstruction.git
```

Если оказалось так что надо ДОБАВИТЬ сабмодули(забыли `--recurse-submodules` или чекаутнулись в ветку с новыми сабмодулями) - выполняем следующее

```
git submodule init
git submodule update
```