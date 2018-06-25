#!/bin/bash


function usage() {
  echo "Usage:"
  echo "$0 [ -d <encrypted_text> -k <key-id> | -e <plaintext> ]"
}

while getopts ':hd:e:k:' option; do
  case "$option" in
    h) usage
       exit
       ;;
    d) CIPHER_TEXT="$OPTARG"
       ;;
    e) PLAIN_TEXT="$OPTARG"
       ;;
    k) KEY_ID="$OPTARG"
       ;;
    :) echo "missing argument for -$OPTARG" >&2
       usage
       exit 1
       ;;
   \?) echo "Invalid option: -$OPTARG" >&2
       usage
       exit 1
       ;;
  esac
done
shift $((OPTIND - 1))


if [[ ! -z "$PLAIN_TEXT" && ! -z "$CIPHER_TEXT" ]]; then
	echo "Can only use one option: -e or -d"
	usage
	exit 1
fi


function encrypt () {
    ENCRYPTED=$(aws kms encrypt --key-id $KEY_ID --plaintext $PLAIN_TEXT --output text --query CiphertextBlob)
    echo "$ENCRYPTED"
}

function decrypt () {
    BASE64_ENC_CIPHER="/tmp/$(date +%Y%m%d_%H%M%S)_kmshelper"
    echo "$CIPHER_TEXT" | base64 --decode > $BASE64_ENC_CIPHER
    DECRYPTED=$(aws kms decrypt --ciphertext-blob fileb://$BASE64_ENC_CIPHER --output text --query Plaintext | base64 --decode)
    echo "$DECRYPTED"
}


if [[ ! -z "$PLAIN_TEXT" ]]; then
    if [[ -z "$KEY_ID" ]]; then
	echo "You need to provide a KMS key-ID"
	usage
	exit 1
    fi
    encrypt
elif [[ ! -z "$CIPHER_TEXT" ]]; then
    decrypt
fi
