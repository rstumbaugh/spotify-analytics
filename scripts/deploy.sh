#! /bin/bash

app_name=spotify-elastic
root=~/Development/repos/spotify-elastic
venv_path=~/Development/envs/spotify-analytics
version_path=$root/__version__

ssh_key=~/Development/keys/aws/rstum.pem
user=ec2-user
host=ec2-54-175-95-178.compute-1.amazonaws.com
ec2_output_dir="/home/$user"
ec2_env_path="/home/$user/env"

# array contains function
function contains() {
    local n=$#
    local value=${!n}
    for ((i=1;i < $#;i++)) {
        if [ "${!i}" == "${value}" ]; then
            return 0
        fi
    }
    return 1
}

cd $root

# get latest version from version file
echo [deploy] Loading latest version...
new_version=`scripts/get_next_version.sh $version_path`
echo [deploy] New version = $new_version

# copy contents to new verion directory
echo [deploy] Making directory for new version

dir_name=$app_name'_'$new_version
mkdir $dir_name

echo [deploy] Copying contents to $dir_name

hidden=.*
nonhidden=*
ignore=( . .. .git .gitignore .vscode __pycache__ $dir_name )
all=( ${hidden[@]} ${nonhidden[@]} )

for x in ${all[@]}; do
    contains ${ignore[@]} $x
    if [[ $? == 1 ]]; then
        cp -r $x $dir_name
    else
        echo [deploy] Ignoring $x
    fi
done
echo [deploy] Copied contents to $dir_name

ec2_venv_dir=$ec2_env_path/$app_name
ec2_app_dir=$ec2_output_dir/$dir_name

# generate service file in output directory
service_name=$app_name.service
scripts/generate_service.sh \
    $ec2_venv_dir/bin/python3 \
    $ec2_app_dir/main.py \
    $dir_name/$service_name \
    $ec2_output_dir/log/$service_name'_'$new_version.log

# get pip packages for environment
source $venv_path/bin/activate
pip freeze > $dir_name/requirements.txt

# zip output directory for upload
archive_name=`echo $dir_name | sed -e 's/\./_/g'`.zip
echo [deploy] Zipping $dir_name to $archive_name
zip -r $archive_name $dir_name > /dev/null

# copy package to server
echo [deploy] Copying $dir_name.zip to EC2 server
scp -i $ssh_key $archive_name $user@$host:$ec2_output_dir

echo [deploy] Unzipping package and creating environment
ssh -i $ssh_key $user@$host "
    unzip -o $archive_name > /dev/null;
    rm $archive_name;
    $ec2_app_dir/scripts/init_env.sh $ec2_venv_dir $ec2_app_dir;
    $ec2_app_dir/scripts/install_service.sh $service_name $ec2_app_dir
"

# clean up
echo [deploy] Removing $dir_name, $archive_name, $service_name
rm -rf $dir_name $archive_name $service_name

echo [deploy] Done