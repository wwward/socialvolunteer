SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='TRADITIONAL,ALLOW_INVALID_DATES';

CREATE SCHEMA IF NOT EXISTS `groupwerk` DEFAULT CHARACTER SET latin1 ;
USE `groupwerk` ;

-- -----------------------------------------------------
-- Table `groupwerk`.`Friends`
-- -----------------------------------------------------
CREATE  TABLE IF NOT EXISTS `groupwerk`.`Friends` (
  `id` VARCHAR(255) NULL DEFAULT NULL ,
  `friend_id` VARCHAR(255) NULL DEFAULT NULL ,
  INDEX `Idx_friends` (`id` ASC) )
ENGINE = InnoDB
DEFAULT CHARACTER SET = latin1;


-- -----------------------------------------------------
-- Table `groupwerk`.`Job`
-- -----------------------------------------------------
CREATE  TABLE IF NOT EXISTS `groupwerk`.`Job` (
  `id` INT(11) NOT NULL AUTO_INCREMENT ,
  `organization_id` VARCHAR(255) NULL DEFAULT NULL ,
  `event_date` DATE NULL DEFAULT NULL ,
  `event_time` TIME NULL DEFAULT NULL ,
  `event_duration_minutes` SMALLINT(6) NULL DEFAULT NULL ,
  `difficulty` SMALLINT(6) NULL DEFAULT '0' ,
  `score_value` SMALLINT(6) NULL DEFAULT NULL ,
  `title` VARCHAR(100) NULL DEFAULT NULL ,
  `description` TEXT NULL DEFAULT NULL ,
  `location` VARCHAR(100) NULL DEFAULT NULL ,
  `category` VARCHAR(255) NULL DEFAULT NULL ,
  `status` SMALLINT(6) NULL DEFAULT NULL ,
  PRIMARY KEY (`id`) )
ENGINE = InnoDB
AUTO_INCREMENT = 10011
DEFAULT CHARACTER SET = latin1;


-- -----------------------------------------------------
-- Table `groupwerk`.`Job_volunteer`
-- -----------------------------------------------------
CREATE  TABLE IF NOT EXISTS `groupwerk`.`Job_volunteer` (
  `job_id` INT NULL DEFAULT NULL ,
  `volunteer_id` VARCHAR(255) NULL DEFAULT NULL ,
  `committed` SMALLINT(6) NULL DEFAULT NULL ,
  `completed` SMALLINT(6) NULL DEFAULT NULL ,
  `checkedin` SMALLINT(6) NULL DEFAULT NULL ,
  `checkedout` SMALLINT(6) NULL DEFAULT NULL ,
  `modified` DATETIME NULL DEFAULT NULL )
ENGINE = InnoDB
DEFAULT CHARACTER SET = latin1;


-- -----------------------------------------------------
-- Table `groupwerk`.`Keyword`
-- -----------------------------------------------------
CREATE  TABLE IF NOT EXISTS `groupwerk`.`Keyword` (
  `keyword` VARCHAR(30) NOT NULL ,
  `reference_id` INT(11) NOT NULL ,
  INDEX `Idx_keyword` (`keyword` ASC) )
ENGINE = InnoDB
DEFAULT CHARACTER SET = latin1;


-- -----------------------------------------------------
-- Table `groupwerk`.`Organization`
-- -----------------------------------------------------
CREATE  TABLE IF NOT EXISTS `groupwerk`.`Organization` (
  `id` VARCHAR(255) NOT NULL ,
  `name` VARCHAR(60) NULL DEFAULT NULL ,
  `phone` VARCHAR(15) NULL DEFAULT NULL ,
  `email` VARCHAR(60) NULL DEFAULT NULL ,
  `location` VARCHAR(60) NULL DEFAULT NULL ,
  `reputation` SMALLINT(6) NULL DEFAULT NULL ,
  `description` VARCHAR(100) NULL DEFAULT NULL ,
  INDEX `Idx_organization` (`location` ASC) ,
  PRIMARY KEY (`id`) )
ENGINE = InnoDB
AUTO_INCREMENT = 5003
DEFAULT CHARACTER SET = latin1;


-- -----------------------------------------------------
-- Table `groupwerk`.`Score`
-- -----------------------------------------------------
CREATE  TABLE IF NOT EXISTS `groupwerk`.`Score` (
  `id` VARCHAR(255) NULL DEFAULT NULL ,
  `job_id` INT NULL DEFAULT NULL ,
  `score` SMALLINT(6) NULL DEFAULT NULL ,
  INDEX `Idx_score` (`id` ASC) )
ENGINE = InnoDB
DEFAULT CHARACTER SET = latin1;


-- -----------------------------------------------------
-- Table `groupwerk`.`Volunteer`
-- -----------------------------------------------------
CREATE  TABLE IF NOT EXISTS `groupwerk`.`Volunteer` (
  `id` VARCHAR(255) NOT NULL ,
  `name` VARCHAR(60) NULL DEFAULT NULL ,
  `email` VARCHAR(60) NULL DEFAULT NULL ,
  `phone` VARCHAR(15) NULL DEFAULT NULL ,
  `location` VARCHAR(60) NULL DEFAULT NULL ,
  `reputation` SMALLINT(6) NULL DEFAULT NULL ,
  `username` VARCHAR(30) NULL DEFAULT NULL ,
  PRIMARY KEY (`id`) ,
  INDEX `Idx_volunteer` (`location` ASC) )
ENGINE = InnoDB
AUTO_INCREMENT = 1005
DEFAULT CHARACTER SET = latin1;



SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;
