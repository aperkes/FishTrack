for i in $(cat $1); do
ssh $i << EOF
    raspistill -o ~/Desktop/CCtest/test.jpg
    exit
EOF
scp $i:~/Desktop/CCtest/test.jpg ./test_imgs/$i.jpg

done
