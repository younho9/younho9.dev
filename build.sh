# build.sh
pip install pipenv

echo -------------------------------------------------------
echo 🧱 Start build
echo -------------------------------------------------------

cd notion
pipenv install

echo -------------------------------------------------------
echo 📝 Get blog posts from notion
echo -------------------------------------------------------

pipenv run python main.py
cd ..

echo -------------------------------------------------------
echo 💄 Apply prettier
echo -------------------------------------------------------

npx prettier --write content/posts/**/*.md

echo -------------------------------------------------------
echo ✅ Successfully formatted
echo -------------------------------------------------------

echo -------------------------------------------------------
echo 🚗 Run gatsby server
echo -------------------------------------------------------

gatsby develop
