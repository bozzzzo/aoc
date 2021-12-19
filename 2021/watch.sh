while true;
do
	changed="$(git status --porcelain=v2 | grep -v '^\?' || true)"
	if [ "$changed" == "" ]; then
		sleep 1
		continue
	fi
        clear
	git add -u
	git commit -m "$(date)"
	python x.py
done
