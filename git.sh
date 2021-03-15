if [ "$1" != "" ]; then
  case "$1" in
    origin)
      git add --all
      if [ "$2" != "" ]; then
        git commit -m "$2"
      else
        version=$(awk -F ":" '/versnr/ {print $2}' version.json)
        version=${version:1:7}
        git commit -m "undocumented Changes of Version $version"
      fi  
      echo "======================"
      echo "Hochladen mit:"
      echo "git push origin master"
      echo "======================"
      ;;
  esac
else
  echo "Bitte Übergabeparameter angeben: origin, showversion, upversion"
fi
