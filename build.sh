# build.sh
pip install pipenv

echo -------------------------------------------------------
echo 🧱 Start build
cd notion
pipenv install

echo -------------------------------------------------------
echo 📝 Get blog posts from notion
pipenv run python main.py
cd ..

echo -------------------------------------------------------
echo 💄 Apply prettier
npx prettier --write content/posts/**/*.md
echo ✅ Successfully formatted

echo -------------------------------------------------------
echo 🚗 Run gatsby server

gatsby develop
