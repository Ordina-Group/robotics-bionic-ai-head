unameOut="$(uname -s)"
case "${unameOut}" in
    Linux*)     pkill -9 -f .py;;
    *)          TASKKILL //F //IM python*
esac


