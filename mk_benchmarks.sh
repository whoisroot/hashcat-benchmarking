#!/bin/bash

benchmark="--benchmark"
output_dir="benchmarks"
runs=5

function print_usage() {
	echo -e "\nUsage: $0 [-o output_dir] [-a] [-m mode] [-h] [-n num_benchmarks] [-e \"--extra --hashcat --parameters\"]\n"
	echo -e "\tUse -a to run the full benchmark suite. Otherwise, just the default tests are run."
	echo -e "\tYou can pass extra options to hashcat (like -O or -w) using -e."
	echo -e "\tExtra options should always be between quotes, as a single argument".
	echo -e "\tThe default value for -n is 5 runs when not set."
}

while [[ "${1}" != "" ]]; do
	case "${1}" in
		-a)
			benchmark="--benchmark --benchmark-all"
			;;
		-o) 
			output_dir="$2"
			shift 1
			;;
		-m)
			mode="-m $2"
			shift 1
			;;
		-h)
			print_usage
			exit 0
			;;
		-n)
			runs=$2
			shift 1
			;;
		-e)
			extras="$2"
			shift 1
			;;
		*)
			print_usage
			exit 1
			;;
	esac
	shift 1
done

if [[ "${benchmark}" = "benchmarks" ]]; then
	print_usage
	echo -e "Continue?\n"
	printf "Y/[N]: "
	read answer

	if [[ "${answer}" = "Y" || "${answer}" = "y" ]]; then
		true
	else
		exit 0
	fi
fi

if [[ -e "${output_dir}/benchmark_1.txt" ]]; then
	echo -e "\nWARNING: Output directory \"${output_dir}\" already exists!"
	echo -e "You can define a new directory with -o \"new_directory\"."
	echo -e "Do you wish to continue and overwrite it?\n"
	printf "Y/[N]: "
	read answer
	
	if [[ "${answer}" = "Y" || "${answer}" = "y" ]]; then
		true
	else
		exit 0
	fi
fi

if [[ ! -d "${output_dir}" ]]; then
	mkdir -p "${output_dir}"
fi

start_time="$(date '+%F %T')"

for i in $(seq -w ${runs}); do
	echo -e -n "\n\t"
	printf -- '#%.0s' $(seq -w $(( ${#runs} + 14 )))
	echo -e "\n\t# Benchmark $i #"
	echo -e -n "\t"
	printf -- '#%.0s' $(seq -w $(( ${#runs} + 14 )))
	echo -e "\n"
	date '+%F %T'
	echo

	outfile="${output_dir}/benchmark_$i"

	hashcat ${benchmark} ${mode} --machine-readable ${extras} | tee "${outfile}.txt"
	./parser.py "${outfile}.txt" "${outfile}.json"
done

end_time="$(date '+%F %T')"

echo -e "\n###################################"
echo -e "# Start time: ${start_time} #\n# End time: ${end_time}   #"
echo -e "###################################\n"

echo "Merging hashcat benchmarks..."
benchmarks="$(printf -- "\"${output_dir}/benchmark_%s.json\" " $(seq -w ${runs}))"
bash -c "./merger.py -o \"$output_dir/merged.json\" ${benchmarks}"
echo -e "\nTo compare results use\n./comparator.py [-o outfile.json] benchmark_a/merged.json benchmark_b/merged.json\n"
