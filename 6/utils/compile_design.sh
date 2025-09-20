#!/bin/bash

#---------------------------------------------------------------------------------
#   set defaults
#---------------------------------------------------------------------------------
set_defaults() {
    script_version=0.3
    sim_dir=$(pwd)
    # timeout=60
    pre_script="pre_compile_design.sh"
    post_script="post_compile_design.sh"
    fw_script_dir="../../design/design_units/top/source/scripts/"
    script_file="fps.sh"
    log_file="fps.log"
    # questa_version=""
    lib_file=""
}

#---------------------------------------------------------------------------------
#   Get Options
#---------------------------------------------------------------------------------
get_options() {
    while [[ $# -gt 0 ]]; do
        case $1 in
            # -q|-questa      ) questa_version="$2" ; shift;;
            -v|-vendor      ) vendor="$2"         ; shift;;
            # -t|-timeout     ) timeout="$2"        ; shift;;
            -h|-help        ) print_help                 ;;
            -b|-build       ) build_flag=1              ;;
            -c|-compile     ) compile_flag=1            ;;
            *               ) print_help "$1"
        esac
        shift
    done
}

#---------------------------------------------------------------------------------
#   print help
#---------------------------------------------------------------------------------
print_help() {
    echo -e "\n-------------------------------------------------------------------------------------\n"
    echo -e "\e[1mScript version: $script_version\e[0m\n"

    echo -e "\e[4mUsage:\n\e[0m    bash $0 -v vivado\n"

    echo -e "\e[4mAvailable options are:\e[0m"
    echo -e "   -v | -vendor <vivado/altera>       -- Set vivado (=xilinx) or quartus (=altera). (mandatory) "
    echo -e "   -h | -help                         -- Print help menu\n"
    echo -e "   -b | -build                        -- Trigger build action\n"
    echo -e "   -c | -compile                      -- Trigger compile action\n"

    echo -e "\n-------------------------------------------------------------------------------------\n"

    exit 0
}

#---------------------------------------------------------------------------------
#   check args
#---------------------------------------------------------------------------------
check_args(){
    if [[ "$vendor" != "vivado" && "$vendor" != "quartus" ]]; then
        echo "Compile_design error: vendor $vendor is neither 'vivado' nor 'quartus'"
        exit 1
    fi
    
    if [ $vendor = "vivado" ]; then
        lib_file="elaborate.do"
        lib_string=" *vopt"
        lib_dir_name="questa_lib"
    elif [ $vendor = "quartus" ]; then
        lib_file="msim_setup.tcl"
        lib_string=" *eval vsim"
        lib_dir_name="libraries"
    else
        echo "Compile_design error: Invalid lib_file"
        exit 1
    fi
    
}

#---------------------------------------------------------------------------------
#   run script 
#---------------------------------------------------------------------------------
run_script(){
    # Check if the fw_script_dir exists
    if [ -d "$fw_script_dir" ]; then
        cd "$fw_script_dir"
    else
        echo "Compile_design error: $fw_script_dir doesn't exist. Check your design dir"
        exit 1
    fi

    # # Questa version - update only if user didn't give its version
    # if [ -z "$questa_version" ]; then
    #     questa_version=$(grep "set *questa_version" ${vendor}/${vendor}_project_settings.tcl  | sed 's/.*set *questa_version//' | sed 's/ *//')
    #     echo "Compile_design info: questa_version from FW scripts (${vendor}/${vendor}_project_settings.tcl) is $questa_version"
    # else
    #     echo "Compile_design info: questa_version from user input is $questa_version"
    # fi
    
    chmod -R 755 *

    if [ "$build_flag" ]; then
        echo "Compile_design info: run $script_file $vendor build"
        bash $script_file -$vendor -b -o -force
    fi

    if [ -f $sim_dir/$pre_script ]; then
        echo "Compile_design info: call $pre_script"
        bash $sim_dir/$pre_script
    fi

    if [ "$compile_flag" ]; then
    	echo "Compile_design info: run $script_file $vendor compile"
    	bash $script_file -$vendor -c -o  
    fi

    echo "Compile_design info: Update vopt_libraries"
    libraries=$(find ../../build/simulation/$vendor/ -type f -name $lib_file 2>/dev/null)
    if [ -z "$libraries" ]; then
        echo "Compile_design error: No files found matching $lib_file in ../../build/simulation/$vendor/"
        exit 1
    else
        echo "Compile_design info: Found file: $libraries"
    fi

    libs_temp=$(grep "^$lib_string" $libraries | head -n 1 | awk '{ for(i=1; i<=NF; i++) if ($i ~ /^-L/) print $i, $(i+1) }')
    libs=($(echo $libs_temp | tr '\n' ' '))
    echo "Compile_design info: libraries are ${libs[@]}"

    glbl=$(grep "^$lib_string" $libraries | awk '{ for(i=1; i<=NF; i++) if ($i ~ /glbl/) print $i }')
    if [ -n "$glbl" ]; then
        echo "Compile_design info: glbl is $glbl"
    fi

    modelsim=$(find ../../build/simulation/$vendor/ -type f -name modelsim.ini 2>/dev/null)
    if [ -z "$modelsim" ]; then
        echo "Compile_design error: No files found matching modelsim.ini in ../../build/simulation/$vendor/"
        exit 1
    else
        echo "Compile_design info: Modelsim file: $modelsim"
    fi

    lib_dir=$(find ../../build/simulation/$vendor/ -type d -name $lib_dir_name 2>/dev/null)
    if [ -z "$lib_dir" ]; then
        echo "Compile_design error: No dirs found matching $lib_dir_name ../../build/simulation/$vendor/"
        exit 1
    else
        echo "Compile_design info: Found lib_dir: $lib_dir"
    fi

    cd $sim_dir
    echo "Compile_design info: Update $sim_dir"

    libs=$(echo ${libs[@]} | tr -d '{}')

    cp -f $fw_script_dir/$modelsim .

    for src in "$fw_script_dir/$lib_dir"/../*; do
      target=$(basename "$src")
      # Skip if this is modelsim.ini - hard copied before
      if [ "$target" == "modelsim.ini" ]; then
        continue
      fi

      # If target is an existing symlink/file/dir, ignore it
      if [ -e "$target" ]; then
        echo "Compile_design info: Overwriting existing $target with new link"
        rm -rf "$target"  
      fi

      # Create new symlink
      ln -sf "$src" "$target"
    done


    if [ -f $sim_dir/$post_script ]; then
        echo "Compile_design info: call $post_script"
        bash $sim_dir/$post_script
    fi

    echo "Compile_design summary: vopt libs are $libs $glbl"
    echo "Compile_design info: done"

}

#---------------------------------------------------------------------------------
#   RUN
#---------------------------------------------------------------------------------
set_defaults
get_options "$@"
check_args
run_script
