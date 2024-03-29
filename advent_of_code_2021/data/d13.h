//
// Created by bsaund on 12/13/21.
//

#ifndef ADVENT_OF_CODE_2021_D13_H
#define ADVENT_OF_CODE_2021_D13_H

std::string data_str = "176,226\n"
                       "749,474\n"
                       "1218,784\n"
                       "1193,451\n"
                       "478,224\n"
                       "1019,620\n"
                       "865,667\n"
                       "884,178\n"
                       "622,505\n"
                       "43,856\n"
                       "475,619\n"
                       "1295,96\n"
                       "497,499\n"
                       "589,326\n"
                       "117,267\n"
                       "559,361\n"
                       "402,863\n"
                       "1220,277\n"
                       "167,617\n"
                       "955,560\n"
                       "1011,135\n"
                       "311,618\n"
                       "865,198\n"
                       "855,761\n"
                       "698,241\n"
                       "180,786\n"
                       "728,523\n"
                       "832,222\n"
                       "865,67\n"
                       "1280,649\n"
                       "155,844\n"
                       "990,406\n"
                       "688,505\n"
                       "990,488\n"
                       "1116,288\n"
                       "1047,266\n"
                       "181,408\n"
                       "27,401\n"
                       "883,257\n"
                       "253,610\n"
                       "1213,131\n"
                       "967,395\n"
                       "581,605\n"
                       "316,302\n"
                       "1260,425\n"
                       "967,171\n"
                       "721,774\n"
                       "618,668\n"
                       "604,51\n"
                       "858,323\n"
                       "520,553\n"
                       "271,730\n"
                       "749,567\n"
                       "1274,892\n"
                       "1054,102\n"
                       "117,301\n"
                       "201,598\n"
                       "227,257\n"
                       "1193,267\n"
                       "146,658\n"
                       "87,498\n"
                       "1017,313\n"
                       "1211,628\n"
                       "118,668\n"
                       "1059,259\n"
                       "48,169\n"
                       "698,292\n"
                       "405,516\n"
                       "676,110\n"
                       "1101,667\n"
                       "298,453\n"
                       "251,119\n"
                       "1046,529\n"
                       "1245,774\n"
                       "1019,722\n"
                       "1009,365\n"
                       "117,593\n"
                       "27,469\n"
                       "599,164\n"
                       "915,775\n"
                       "1088,91\n"
                       "530,407\n"
                       "124,571\n"
                       "494,378\n"
                       "97,59\n"
                       "995,443\n"
                       "311,49\n"
                       "345,822\n"
                       "175,469\n"
                       "174,560\n"
                       "427,66\n"
                       "261,120\n"
                       "371,38\n"
                       "73,844\n"
                       "145,637\n"
                       "674,675\n"
                       "1275,646\n"
                       "787,44\n"
                       "1074,57\n"
                       "478,229\n"
                       "1140,630\n"
                       "999,51\n"
                       "559,252\n"
                       "30,649\n"
                       "1256,182\n"
                       "836,882\n"
                       "801,679\n"
                       "271,394\n"
                       "176,665\n"
                       "989,211\n"
                       "887,533\n"
                       "431,147\n"
                       "760,539\n"
                       "1207,523\n"
                       "73,172\n"
                       "786,690\n"
                       "504,674\n"
                       "1039,858\n"
                       "1034,702\n"
                       "540,277\n"
                       "457,89\n"
                       "393,436\n"
                       "995,397\n"
                       "728,371\n"
                       "556,850\n"
                       "180,747\n"
                       "345,72\n"
                       "887,361\n"
                       "484,742\n"
                       "692,598\n"
                       "835,619\n"
                       "1057,158\n"
                       "1159,891\n"
                       "412,201\n"
                       "801,33\n"
                       "391,628\n"
                       "1116,736\n"
                       "1240,344\n"
                       "530,487\n"
                       "667,397\n"
                       "639,171\n"
                       "880,168\n"
                       "390,813\n"
                       "788,176\n"
                       "1250,793\n"
                       "780,487\n"
                       "445,667\n"
                       "1217,857\n"
                       "832,705\n"
                       "42,763\n"
                       "813,499\n"
                       "700,444\n"
                       "114,619\n"
                       "1191,884\n"
                       "119,10\n"
                       "791,313\n"
                       "917,436\n"
                       "1243,343\n"
                       "1290,513\n"
                       "15,798\n"
                       "728,75\n"
                       "179,833\n"
                       "683,873\n"
                       "773,260\n"
                       "830,271\n"
                       "567,620\n"
                       "610,450\n"
                       "395,567\n"
                       "231,361\n"
                       "1135,469\n"
                       "1278,46\n"
                       "1136,399\n"
                       "780,357\n"
                       "403,567\n"
                       "671,778\n"
                       "343,51\n"
                       "902,78\n"
                       "676,241\n"
                       "345,486\n"
                       "504,224\n"
                       "136,593\n"
                       "458,400\n"
                       "806,224\n"
                       "274,873\n"
                       "753,347\n"
                       "591,714\n"
                       "699,856\n"
                       "966,427\n"
                       "991,773\n"
                       "169,859\n"
                       "85,339\n"
                       "817,175\n"
                       "470,733\n"
                       "932,52\n"
                       "378,310\n"
                       "164,694\n"
                       "999,619\n"
                       "552,168\n"
                       "523,44\n"
                       "807,303\n"
                       "843,623\n"
                       "999,299\n"
                       "160,826\n"
                       "97,723\n"
                       "557,347\n"
                       "790,553\n"
                       "1143,617\n"
                       "701,637\n"
                       "1109,598\n"
                       "1193,515\n"
                       "418,505\n"
                       "522,649\n"
                       "184,733\n"
                       "801,705\n"
                       "227,42\n"
                       "1255,235\n"
                       "222,159\n"
                       "92,784\n"
                       "95,364\n"
                       "912,344\n"
                       "85,787\n"
                       "1170,511\n"
                       "756,809\n"
                       "473,184\n"
                       "226,731\n"
                       "676,513\n"
                       "1130,108\n"
                       "251,775\n"
                       "219,484\n"
                       "219,708\n"
                       "151,357\n"
                       "1192,674\n"
                       "360,505\n"
                       "1267,486\n"
                       "972,592\n"
                       "626,221\n"
                       "1268,292\n"
                       "445,248\n"
                       "830,495\n"
                       "69,143\n"
                       "401,485\n"
                       "1213,884\n"
                       "1175,313\n"
                       "1241,303\n"
                       "612,627\n"
                       "634,676\n"
                       "947,620\n"
                       "729,498\n"
                       "721,326\n"
                       "1299,451\n"
                       "544,537\n"
                       "1079,306\n"
                       "373,172\n"
                       "1036,873\n"
                       "519,357\n"
                       "1163,203\n"
                       "1197,268\n"
                       "802,147\n"
                       "95,585\n"
                       "181,413\n"
                       "858,213\n"
                       "604,537\n"
                       "452,323\n"
                       "662,488\n"
                       "276,401\n"
                       "1178,357\n"
                       "743,128\n"
                       "236,57\n"
                       "1210,309\n"
                       "905,516\n"
                       "99,492\n"
                       "430,168\n"
                       "1083,637\n"
                       "706,625\n"
                       "345,408\n"
                       "569,555\n"
                       "831,61\n"
                       "32,400\n"
                       "1208,352\n"
                       "892,505\n"
                       "97,884\n"
                       "58,7\n"
                       "227,852\n"
                       "1143,572\n"
                       "643,751\n"
                       "311,548\n"
                       "12,450\n"
                       "276,394\n"
                       "505,707\n"
                       "370,355\n"
                       "599,659\n"
                       "445,67\n"
                       "557,884\n"
                       "1211,154\n"
                       "1084,137\n"
                       "1238,523\n"
                       "551,747\n"
                       "264,589\n"
                       "755,850\n"
                       "887,431\n"
                       "311,845\n"
                       "27,465\n"
                       "254,814\n"
                       "102,726\n"
                       "10,750\n"
                       "184,676\n"
                       "676,784\n"
                       "831,541\n"
                       "1039,500\n"
                       "937,172\n"
                       "140,607\n"
                       "831,353\n"
                       "479,61\n"
                       "264,813\n"
                       "259,119\n"
                       "840,733\n"
                       "239,262\n"
                       "1136,750\n"
                       "68,341\n"
                       "1275,248\n"
                       "445,26\n"
                       "766,537\n"
                       "1265,396\n"
                       "1098,53\n"
                       "774,668\n"
                       "50,537\n"
                       "152,175\n"
                       "118,674\n"
                       "472,331\n"
                       "1283,401\n"
                       "1299,443\n"
                       "1163,691\n"
                       "1012,493\n"
                       "909,50\n"
                       "639,723\n"
                       "870,393\n"
                       "975,185\n"
                       "1212,492\n"
                       "229,777\n"
                       "1310,172\n"
                       "627,149\n"
                       "42,292\n"
                       "1206,287\n"
                       "136,145\n"
                       "97,131\n"
                       "11,443\n"
                       "671,171\n"
                       "335,325\n"
                       "686,549\n"
                       "44,444\n"
                       "1059,119\n"
                       "1208,726\n"
                       "197,420\n"
                       "1120,301\n"
                       "753,803\n"
                       "1215,642\n"
                       "975,709\n"
                       "564,281\n"
                       "197,474\n"
                       "207,150\n"
                       "805,707\n"
                       "552,253\n"
                       "144,563\n"
                       "556,716\n"
                       "1083,497\n"
                       "503,357\n"
                       "271,500\n"
                       "1268,602\n"
                       "145,215\n"
                       "756,163\n"
                       "290,296\n"
                       "589,120\n"
                       "1176,341\n"
                       "691,198\n"
                       "535,296\n"
                       "962,625\n"
                       "296,574\n"
                       "555,873\n"
                       "445,446\n"
                       "171,722\n"
                       "932,584\n"
                       "944,401\n"
                       "955,807\n"
                       "580,479\n"
                       "723,103\n"
                       "355,334\n"
                       "910,814\n"
                       "73,624\n"
                       "971,3\n"
                       "698,653\n"
                       "202,547\n"
                       "1295,723\n"
                       "1083,66\n"
                       "283,436\n"
                       "65,777\n"
                       "295,738\n"
                       "751,361\n"
                       "1190,750\n"
                       "519,177\n"
                       "991,26\n"
                       "494,826\n"
                       "95,82\n"
                       "1084,731\n"
                       "1083,257\n"
                       "1027,436\n"
                       "1213,579\n"
                       "75,150\n"
                       "792,77\n"
                       "518,77\n"
                       "704,171\n"
                       "72,523\n"
                       "1116,158\n"
                       "306,513\n"
                       "388,65\n"
                       "315,443\n"
                       "97,619\n"
                       "93,663\n"
                       "282,892\n"
                       "112,254\n"
                       "134,647\n"
                       "373,274\n"
                       "113,268\n"
                       "69,420\n"
                       "151,751\n"
                       "426,626\n"
                       "1178,494\n"
                       "473,486\n"
                       "1211,413\n"
                       "1119,465\n"
                       "519,313\n"
                       "691,795\n"
                       "535,598\n"
                       "170,712\n"
                       "831,93\n"
                       "1299,133\n"
                       "1266,444\n"
                       "937,786\n"
                       "125,184\n"
                       "718,813\n"
                       "423,431\n"
                       "229,290\n"
                       "440,393\n"
                       "1074,281\n"
                       "1197,178\n"
                       "965,72\n"
                       "214,501\n"
                       "263,621\n"
                       "922,9\n"
                       "788,649\n"
                       "306,558\n"
                       "909,284\n"
                       "55,730\n"
                       "1207,371\n"
                       "1198,469\n"
                       "994,302\n"
                       "263,721\n"
                       "311,299\n"
                       "104,287\n"
                       "550,355\n"
                       "391,714\n"
                       "216,331\n"
                       "808,175\n"
                       "1265,498\n"
                       "694,855\n"
                       "749,409\n"
                       "746,613\n"
                       "212,53\n"
                       "378,584\n"
                       "1026,355\n"
                       "145,355\n"
                       "425,604\n"
                       "132,357\n"
                       "557,507\n"
                       "1047,621\n"
                       "1159,3\n"
                       "284,66\n"
                       "1026,592\n"
                       "28,553\n"
                       "257,143\n"
                       "470,228\n"
                       "309,408\n"
                       "315,497\n"
                       "530,805\n"
                       "882,611\n"
                       "1113,420\n"
                       "372,892\n"
                       "1165,705\n"
                       "892,11\n"
                       "1236,479\n"
                       "683,745\n"
                       "20,513\n"
                       "447,150\n"
                       "753,507\n"
                       "1290,558\n"
                       "251,635\n"
                       "721,120\n"
                       "1193,739\n"
                       "60,218\n"
                       "309,486\n"
                       "927,858\n"
                       "509,705\n"
                       "1178,537\n"
                       "320,488\n"
                       "1032,501\n"
                       "618,598\n"
                       "1034,500\n"
                       "344,19\n"
                       "763,858\n"
                       "892,883\n"
                       "1292,667\n"
                       "561,679\n"
                       "99,266\n"
                       "774,226\n"
                       "113,324\n"
                       "627,877\n"
                       "671,723\n"
                       "907,567\n"
                       "1056,841\n"
                       "100,507\n"
                       "253,64\n"
                       "1237,605\n"
                       "38,407\n"
                       "1034,425\n"
                       "654,172\n"
                       "445,491\n"
                       "348,625\n"
                       "1233,128\n"
                       "832,224\n"
                       "445,448\n"
                       "401,284\n"
                       "140,511\n"
                       "554,809\n"
                       "1088,735\n"
                       "567,498\n"
                       "1116,437\n"
                       "1135,751\n"
                       "730,479\n"
                       "581,50\n"
                       "967,51\n"
                       "709,745\n"
                       "370,715\n"
                       "32,46\n"
                       "231,306\n"
                       "209,739\n"
                       "67,343\n"
                       "837,315\n"
                       "1196,723\n"
                       "98,402\n"
                       "1036,425\n"
                       "98,850\n"
                       "1233,340\n"
                       "946,2\n"
                       "1292,227\n"
                       "1225,339\n"
                       "920,529\n"
                       "1283,465\n"
                       "284,539\n"
                       "1079,809\n"
                       "868,53\n"
                       "1059,567\n"
                       "780,537\n"
                       "171,172\n"
                       "1215,812\n"
                       "468,287\n"
                       "1059,635\n"
                       "401,50\n"
                       "479,833\n"
                       "999,49\n"
                       "587,791\n"
                       "611,486\n"
                       "977,824\n"
                       "343,52\n"
                       "1303,284\n"
                       "1017,784\n"
                       "574,526\n"
                       "1165,215\n"
                       "127,722\n"
                       "253,158\n"
                       "512,228\n"
                       "612,205\n"
                       "643,397\n"
                       "927,659\n"
                       "1300,144\n"
                       "1126,676\n"
                       "1299,751\n"
                       "80,424\n"
                       "1200,537\n"
                       "692,296\n"
                       "535,436\n"
                       "641,855\n"
                       "919,714\n"
                       "223,299\n"
                       "725,591\n"
                       "1213,723\n"
                       "658,516\n"
                       "838,331\n"
                       "826,294\n"
                       "1267,856\n"
                       "470,653\n"
                       "97,212\n"
                       "837,710\n"
                       "756,835\n"
                       "831,425\n"
                       "502,175\n"
                       "290,2\n"
                       "319,773\n"
                       "1049,355\n"
                       "919,833\n"
                       "591,845\n"
                       "373,786\n"
                       "636,219\n"
                       "540,802\n"
                       "1257,597\n"
                       "478,222\n"
                       "298,1\n"
                       "28,341\n"
                       "850,9\n"
                       "184,666\n"
                       "251,327\n"
                       "554,835\n"
                       "995,891\n"
                       "848,190\n"
                       "1087,147\n"
                       "1282,553\n"
                       "152,560\n"
                       "1236,415\n"
                       "879,147\n"
                       "674,219\n"
                       "591,180\n"
                       "370,144\n"
                       "293,110\n"
                       "1159,751\n"
                       "940,592\n"
                       "1073,830\n"
                       "97,275\n"
                       "503,21\n"
                       "321,742\n"
                       "1176,647\n"
                       "1243,418\n"
                       "107,858\n"
                       "840,666\n"
                       "281,219\n"
                       "1265,189\n"
                       "97,579\n"
                       "291,620\n"
                       "67,418\n"
                       "749,679\n"
                       "278,501\n"
                       "272,182\n"
                       "319,26\n"
                       "1193,634\n"
                       "6,488\n"
                       "1001,408\n"
                       "1131,61\n"
                       "20,336\n"
                       "666,750\n"
                       "223,147\n"
                       "1255,164\n"
                       "1197,324\n"
                       "20,241\n"
                       "1139,722\n"
                       "940,403\n"
                       "627,45\n"
                       "366,407\n"
                       "363,172\n"
                       "126,668\n"
                       "1004,336\n"
                       "711,164\n"
                       "534,144\n"
                       "773,525\n"
                       "610,444\n"
                       "520,647\n"
                       "6,600\n"
                       "455,133\n"
                       "759,747\n"
                       "766,357\n"
                       "509,355\n"
                       "759,147\n"
                       "692,2\n"
                       "1268,355\n"
                       "530,313\n"
                       "325,119\n"
                       "117,379\n"
                       "711,730\n"
                       "753,91\n"
                       "760,735\n"
                       "1211,292\n"
                       "775,296\n"
                       "420,782\n"
                       "338,592\n"
                       "706,537\n"
                       "465,697\n"
                       "460,9\n"
                       "503,143\n"
                       "428,78\n"
                       "1193,155\n"
                       "1220,617\n"
                       "1217,791\n"
                       "528,226\n"
                       "355,87\n"
                       "1044,885\n"
                       "801,579\n"
                       "536,226\n"
                       "145,539\n"
                       "388,9\n"
                       "551,147\n"
                       "1155,844\n"
                       "1012,45\n"
                       "1260,619\n"
                       "431,523\n"
                       "1034,873\n"
                       "84,873\n"
                       "74,479\n"
                       "691,696\n"
                       "202,213\n"
                       "229,499\n"
                       "353,529\n"
                       "643,451\n"
                       "194,288\n"
                       "169,35\n"
                       "38,39\n"
                       "93,499\n"
                       "54,182\n"
                       "966,19\n"
                       "790,229\n"
                       "170,630\n"
                       "132,89\n"
                       "1215,687\n"
                       "1260,537\n"
                       "1038,40\n"
                       "175,21\n"
                       "55,164\n"
                       "425,731\n"
                       "1101,739\n"
                       "753,884\n"
                       "793,107\n"
                       "321,11\n"
                       "922,829\n"
                       "1081,499\n"
                       "1079,85\n"
                       "883,66\n"
                       "194,736\n"
                       "547,858\n"
                       "356,893\n"
                       "465,197\n"
                       "540,275\n"
                       "791,357\n"
                       "522,89\n"
                       "865,827\n"
                       "38,597\n"
                       "59,75\n"
                       "135,313\n"
                       "50,843\n"
                       "749,215\n"
                       "311,346\n"
                       "378,52\n"
                       "325,775\n"
                       "775,744\n"
                       "669,855\n"
                       "683,149\n"
                       "487,870\n"
                       "1245,120\n"
                       "1081,395\n"
                       "769,122\n"
                       "1282,445\n"
                       "190,301\n"
                       "1178,649\n"
                       "946,892\n"
                       "42,539\n"
                       "1283,493\n"
                       "209,369\n"
                       "1196,171\n"
                       "753,547\n"
                       "529,184\n"
                       "1146,200\n"
                       "823,277\n"
                       "647,284\n"
                       "567,128\n"
                       "107,36\n"
                       "517,787\n"
                       "423,361\n"
                       "644,750\n"
                       "1252,7\n"
                       "333,294\n"
                       "1217,26\n"
                       "1303,610\n"
                       "45,396\n"
                       "175,61\n"
                       "920,813\n"
                       "952,544\n"
                       "522,718\n"
                       "848,359\n"
                       "348,241\n"
                       "1046,589\n"
                       "263,861\n"
                       "791,537\n"
                       "356,1\n"
                       "868,617\n"
                       "1049,774\n"
                       "823,572\n"
                       "301,365\n"
                       "634,381\n"
                       "442,841\n"
                       "1198,254\n"
                       "27,493\n"
                       "1283,849\n"
                       "432,735\n"
                       "33,558\n"
                       "875,708\n"
                       "38,855\n"
                       "770,725\n"
                       "263,609\n"
                       "361,110\n"
                       "1272,39\n"
                       "729,172\n"
                       "363,620\n"
                       "1083,738\n"
                       "908,31\n"
                       "910,53\n"
                       "848,862\n"
                       "1178,89\n"
                       "1010,369\n"
                       "509,691\n"
                       "72,11\n"
                       "69,474\n"
                       "676,676\n"
                       "281,257\n"
                       "1113,474\n"
                       "544,357\n"
                       "1174,593\n"
                       "348,65\n"
                       "38,465\n"
                       "1260,394\n"
                       "760,159\n"
                       "145,189\n"
                       "731,744\n"
                       "266,885\n"
                       "971,397\n"
                       "181,481\n"
                       "634,218\n"
                       "103,523\n"
                       "816,378\n"
                       "1242,789\n"
                       "145,257\n"
                       "999,276\n"
                       "1186,123\n"
                       "\n"
                       "fold along x=655\n"
                       "fold along y=447\n"
                       "fold along x=327\n"
                       "fold along y=223\n"
                       "fold along x=163\n"
                       "fold along y=111\n"
                       "fold along x=81\n"
                       "fold along y=55\n"
                       "fold along x=40\n"
                       "fold along y=27\n"
                       "fold along y=13\n"
                       "fold along y=6";

#endif//ADVENT_OF_CODE_2021_D13_H
