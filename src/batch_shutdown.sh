for i in $(cat $1); do
ssh $i << EOF
    sudo shutdown
    exit
EOF

done
