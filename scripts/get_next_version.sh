#! /bin/bash

# get latest version from version file, increment last number, store & echo new version
version_path=$1
latest_version=`cat $version_path`

if [[ $latest_version =~ ^(([0-9]+\.)+)([0-9]+)$ ]]; then
    version_base=${BASH_REMATCH[1]}
    deployment_num=${BASH_REMATCH[3]}
    new_deployment=$((deployment_num + 1))
    #new_deployment=$deployment_num
    new_version=$version_base$new_deployment

    echo $new_version > $version_path
    echo $new_version
else
    echo Error: $latest_version does not match regex
fi
