#!/data/data/com.termux/files/usr/bin/bash

CONFIG_FILE="$HOME/.ai-haklab/config.json"

show_menu() {
    clear
    echo -e "\e[1;34m"
    echo "  _      _   _       _    _       _     "
    echo " (_)    | | | |     | |  | |     | |    "
    echo "  _     | |_| | __ _| | _| | __ _| |__  "
    echo " | |    |  _  |/ _\` | |/ / |/ _\` | '_ \ "
    echo " | |    | | | | (_| |   <| | (_| | |_) |"
    echo " |_|____|_| |_|\__,_|_|\_\_|\__,_|_.__/ "
    echo "   |______|                             "
    echo -e "           \e[1;36mAI-HAKLAB: CONFIGURACIÓN DE INTELIGENCIA\e[0m"
    echo -e "\e[1;34m------------------------------------------------------------\e[0m"
    
    current=$(jq -r '.current_provider' $CONFIG_FILE)
    echo -e " \e[1;33mProveedor Actual:\e[0m \e[1;32m$current\e[0m"
    echo -e "\e[1;34m------------------------------------------------------------\e[0m"
    
    providers=$(jq -r '.providers | keys[]' $CONFIG_FILE)
    i=1
    declare -a provider_list
    for p in $providers; do
        name=$(jq -r ".providers.\"$p\".name" $CONFIG_FILE)
        key=$(jq -r ".providers.\"$p\".api_key" $CONFIG_FILE)
        status="\e[1;31m[SIN LLAVE]\e[0m"
        [ -n "$key" ] && status="\e[1;32m[CONFIGURADA]\e[0m"
        echo -e " \e[1;36m$i)\e[0m $name $status"
        provider_list[$i]=$p
        ((i++))
    done
    
    echo -e "\e[1;34m------------------------------------------------------------\e[0m"
    echo -e " \e[1;32mS)\e[0m Lanzar AI-Haklab"
    echo -ne "\n\e[1;36mSelecciona un proveedor (1-10) o 'S':\e[0m "
    read opt
    
    if [[ "$opt" =~ ^[0-9]+$ ]] && [ "$opt" -le 10 ]; then
        p_key=${provider_list[$opt]}
        current_key=$(jq -r ".providers.\"$p_key\".api_key" $CONFIG_FILE)
        
        # Activar el proveedor seleccionado
        tmp=$(mktemp)
        jq ".current_provider = \"$p_key\"" $CONFIG_FILE > "$tmp" && mv "$tmp" $CONFIG_FILE
        
        if [ -z "$current_key" ]; then
            echo -ne "\e[1;33mIntroduce la API KEY para $(jq -r ".providers.\"$p_key\".name" $CONFIG_FILE):\e[0m "
            read new_key
            if [ -n "$new_key" ]; then
                tmp=$(mktemp)
                jq ".providers.\"$p_key\".api_key = \"$new_key\"" $CONFIG_FILE > "$tmp" && mv "$tmp" $CONFIG_FILE
            fi
        else
            echo -e "\e[1;32m[!] El modelo $p_key ya tiene una llave configurada.\e[0m"
            echo -ne "¿Deseas actualizarla? (s/N): "
            read up_opt
            if [ "${up_opt,,}" == "s" ]; then
                echo -ne "\e[1;33mIntroduce la NUEVA API KEY:\e[0m "
                read new_key
                tmp=$(mktemp)
                jq ".providers.\"$p_key\".api_key = \"$new_key\"" $CONFIG_FILE > "$tmp" && mv "$tmp" $CONFIG_FILE
            fi
        fi
        show_menu
    elif [ "${opt,,}" == "s" ]; then
        echo -e "\e[1;34mIniciando AI-Haklab...\e[0m"
    else
        show_menu
    fi
}

show_menu
