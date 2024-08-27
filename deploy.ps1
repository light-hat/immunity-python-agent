$branch = $(git branch --show-current)

git fetch origin --tags
git pull origin

$major = 0
$minor = 0
$(git describe --tags $(git rev-list --tags --max-count=1)) -match "[0-9]+\.[0-9]+\.([0-9]+)"
$patch = [int]$Matches[1] + 1
$version = "$($major).$($minor).$($patch)"

Write-Host 'The new version is: ' $version
echo $version > VERSION
git tag -a $version -m $version

git add .
git commit -m "publish version $version"
git push -u origin $branch --follow-tags