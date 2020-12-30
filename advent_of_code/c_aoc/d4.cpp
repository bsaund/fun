#include <fstream>
#include <iostream>
#include <set>
#include <vector>

#include "absl/strings/match.h"
#include "absl/strings/str_join.h"
#include "include/file_parsing.h"
#include "include/utils.h"

std::string tmp_data =
    "ecl:gry pid:860033327 eyr:2020 hcl:#fffffd\n"
    "byr:1937 iyr:2017 cid:147 hgt:183cm\n"
    "\n"
    "iyr:2013 ecl:amb cid:350 eyr:2023 pid:028048884\n"
    "hcl:#cfa07d byr:1929\n"
    "\n"
    "hcl:#ae17e1 iyr:2013\n"
    "eyr:2024\n"
    "ecl:brn pid:760753108 byr:1931\n"
    "hgt:179cm\n"
    "\n"
    "hcl:#cfa07d eyr:2025 pid:166559648\n"
    "iyr:2011 ecl:brn hgt:59in";

std::string tmp_invalid_data =
    "eyr:1972 cid:100\n"
    "hcl:#18171d ecl:amb hgt:170 pid:186cm iyr:2018 byr:1926\n"
    "\n"
    "iyr:2019\n"
    "hcl:#602927 eyr:1967 hgt:170cm\n"
    "ecl:grn pid:012533040 byr:1946\n"
    "\n"
    "hcl:dab227 iyr:2012\n"
    "ecl:brn hgt:182cm pid:021572410 eyr:2020 byr:1992 cid:277\n"
    "\n"
    "hgt:59cm ecl:zzz\n"
    "eyr:2038 hcl:74454a iyr:2023\n"
    "pid:3556412378 byr:2007";

// std::string read_from_file(const std::string &day) {
//    std::ifstream f(day + ".txt");
//    return std::string(std::istreambuf_iterator<char>(f), std::istreambuf_iterator<char>());
//}

void part_1(const std::vector<std::string>& data) {
  std::cout << "--------- PART 1 -----------\n";
  // Part 1

  int valid_count = 0;
  //  std::cout << data.size() << "\n";
  for (std::string line : data) {
    //    sscanf(line.c_str(), "%s:%s");
    //    std::cout << line << "\n\n\n";
    int field_count = 0;
    std::string token;
    size_t pos_start = 0;
    while (pos_start < line.length()) {
      //      std::cout << "pos_start: " << pos_start << "\n";
      auto sep = line.find(' ', pos_start);
      sep = std::min(sep, line.find('\n', pos_start));
      sep = std::min(sep, line.length());
      //      std::cout << "sep: " << sep << "\n";
      std::string field(100, '\0');
      sscanf(line.substr(pos_start, sep).c_str(), "%3c:", field.c_str());
      //      std::cout << "field: " << field << "\n";
      pos_start = sep + 1;

      if (!field.starts_with("cid")) {
        field_count++;
      }
    }
    //    std::cout << field_count << "\n";
    if (field_count == 7) {
      valid_count++;
    }
  }
  std::cout << valid_count << "\n\n\n";
}

void part_2(const std::vector<std::string>& data) {
  std::cout << "\n\n\n--------- PART 2 -----------\n";
  // Part 2

  int valid_count = 0;
  for (const std::string& line : data) {
    int field_count = 0;
    std::set<std::string> valid_fields;
    std::string token;
    size_t pos_start = 0;
    while (pos_start < line.length()) {
      auto sep = line.find(' ', pos_start);
      sep = std::min(sep, line.find('\n', pos_start));
      sep = std::min(sep, line.length());
      //      std::cout << "sep: " << sep << "\n";
      char field_char[10];
      sscanf(line.substr(pos_start, sep - pos_start).c_str(), "%3c:", field_char);
      std::string field(field_char);
      std::string contents_str = line.substr(pos_start + 4, sep - pos_start - 4);
      auto contents = contents_str.c_str();

      pos_start = sep + 1;
      //      std::cout << sep << "\n";

      if (field.starts_with("cid")) {
        continue;
      }

      //      std::cout << field << ": " << contents << "\n";
      if (field.starts_with("byr")) {
        int birth_year;
        sscanf(contents, "%d", &birth_year);
        //        std::cout << "Birth year " << birth_year << "\n";
        if (birth_year < 1920 || birth_year > 2002) {
          continue;
        }
      }
      if (field.starts_with("iyr")) {
        int issue_year;
        sscanf(contents, "%d", &issue_year);
        if (issue_year < 2010 or issue_year > 2020) {
          continue;
        }
      }
      if (field.starts_with("eyr")) {
        int exp_year;
        sscanf(contents, "%d", &exp_year);
        if (exp_year < 2020 or exp_year > 2030) {
          continue;
        }
      }
      if (field.starts_with("hgt")) {
        int height;
        std::string units(10, '\0');
//        std::cout << contents << "\n";
        if(sscanf(contents, "%d%2c", &height, units.c_str()) != 2){
          continue;
        }
        //        std::cout << "Height is " << height << " with units " << units << "\n";
        if (units.starts_with("in")) {
          if (height < 59 or height > 76) {
            continue;
          }
        }
        if (units.starts_with("cm")) {
          if (height < 150 or height > 193) {
            continue;
          }
        }
      }

      if (field.starts_with("hcl")) {
        char color_code[10];
        if(sscanf(contents, "#%s", color_code) == 0){
          continue;
        }
//        std::cout << "color code: " << color_code << "\n";
        std::string s(color_code);
        //        std::cout << s.length() << "\n";
        if (s.length() != 6) {
          continue;
        }
        //        std::cout << s << "\n";
        bool invalid = false;
        for (char c : s) {
          if (not absl::StrContains("abcdef0123456789", c)) {
            invalid = true;
            break;
          }
        }
        if (invalid) {
          continue;
        }
      }

      if (field.starts_with("ecl")) {
        if (contents_str.length() != 3) {
          continue;
        }
        if (not absl::StrContains("amb blu brn gry grn hzl oth", contents_str)) {
          continue;
        }
      }

      if (field.starts_with("pid")) {
        if (contents_str.length() != 9) {
          continue;
        }
        //        std::cout << contents_str << "\n";
        bool invalid = false;
        for (auto c : contents_str) {
          if (not absl::StrContains("0123456789", c)) {
            invalid = true;
            break;
          }
        }
        if (invalid) {
          continue;
        }
      }

      field_count++;
      valid_fields.insert(field);
    }
    if (field_count == 7) {
      valid_count++;
      if (valid_fields.size() != 7) {
        std::cout << "There's our problem\n";
      }
//      std::cout << line << "\n";
    }
  }
  std::cout << valid_count << "\n\n\n";
}

int main() {
  auto data_str = read_from_file("d4");
  // Comment out for running on real data
  //  data_str = tmp_data;
  //  std::cout << data_str << '\n';
//  data_str = tmp_invalid_data;
  auto data = split(data_str, "\n\n");

  part_1(data);
  part_2(data);

  return 0;
}
