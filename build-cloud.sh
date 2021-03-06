#!/bin/bash
#
# Copyright 2022 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

rm -Rf build/src
mkdir build/src
cp serviceaccount.json build/src
cp ingesta.py build/src
cp requirements.txt build/src
gcloud builds submit --tag us-central1-docker.pkg.dev/aplicativo:0.1 build
rm -Rf build/src
